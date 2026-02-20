"""Run the clinical injection simulation using MuJoCo physics.

This script loads the clinical scene MJCF model, runs the injection procedure
simulation, and optionally exports animation data for the web viewer.

Usage:
    python -m simulation.run_simulation
    python -m simulation.run_simulation --export output/animation.json
    python -m simulation.run_simulation --render

Attribution: Simulation framework inspired by mjlab (mujocolab/mjlab).
"""

import argparse
import json
import sys
from pathlib import Path

import mujoco
import numpy as np

# Scene model path relative to this file
MODEL_PATH = Path(__file__).parent / "models" / "clinical_scene.xml"

# Injection procedure timing (seconds)
PHASE_PREPARE = 1.0
PHASE_APPROACH = 2.0
PHASE_POSITION = 1.5
PHASE_INJECT = 2.0
PHASE_HOLD = 1.5
PHASE_WITHDRAW = 1.5
PHASE_MONITOR = 2.0

TOTAL_DURATION = (
    PHASE_PREPARE
    + PHASE_APPROACH
    + PHASE_POSITION
    + PHASE_INJECT
    + PHASE_HOLD
    + PHASE_WITHDRAW
    + PHASE_MONITOR
)


def smooth_interp(t: float) -> float:
    """Smoothstep interpolation for natural motion."""
    t = np.clip(t, 0.0, 1.0)
    return float(t * t * (3.0 - 2.0 * t))


def compute_injection_targets(
    model: mujoco.MjModel,
    phase_time: float,
    phase: str,
) -> np.ndarray:
    """Compute actuator targets for the current injection phase.

    Args:
        model: MuJoCo model instance.
        phase_time: Normalized time within the current phase [0, 1].
        phase: Current phase name.

    Returns:
        Array of actuator control targets (degrees).
    """
    n_actuators = model.nu
    targets = np.zeros(n_actuators)
    t = smooth_interp(phase_time)

    # Actuator indices (matching order in MJCF):
    # 0: doc_r_shoulder_pitch, 1: doc_r_shoulder_yaw
    # 2: doc_r_elbow, 3: doc_r_wrist
    # 4: doc_l_shoulder_pitch, 5: doc_l_elbow
    # 6: nurse_r_shoulder_pitch, 7: nurse_r_elbow
    # 8: nurse_l_shoulder_pitch, 9: nurse_l_elbow
    # 10: pat_r_shoulder, 11: pat_r_elbow

    if phase == "prepare":
        # Doctor raises syringe hand to ready position
        targets[0] = t * 30.0  # shoulder pitch
        targets[2] = t * 60.0  # elbow flex
        targets[3] = t * 10.0  # wrist adjust
        # Nurse holds tablet at reading position
        targets[6] = t * 20.0
        targets[7] = t * 70.0

    elif phase == "approach":
        # Doctor extends arm toward patient
        targets[0] = 30.0 + t * 40.0  # shoulder forward
        targets[1] = t * (-30.0)  # shoulder inward
        targets[2] = 60.0 + t * 20.0  # elbow more
        targets[3] = 10.0 + t * 15.0  # wrist fine adjust
        # Nurse steady
        targets[6] = 20.0
        targets[7] = 70.0

    elif phase == "position":
        # Doctor positions needle at deltoid
        targets[0] = 70.0 + t * 5.0
        targets[1] = -30.0 - t * 10.0
        targets[2] = 80.0 + t * 10.0
        targets[3] = 25.0 + t * 5.0
        targets[6] = 20.0
        targets[7] = 70.0

    elif phase == "inject":
        # Hold position, syringe moves inward
        targets[0] = 75.0
        targets[1] = -40.0 - t * 5.0
        targets[2] = 90.0
        targets[3] = 30.0 - t * 5.0
        targets[6] = 20.0
        targets[7] = 70.0

    elif phase == "hold":
        # Steady hold during medication delivery
        targets[0] = 75.0
        targets[1] = -45.0
        targets[2] = 90.0
        targets[3] = 25.0
        targets[6] = 20.0
        targets[7] = 70.0

    elif phase == "withdraw":
        # Doctor withdraws syringe
        targets[0] = 75.0 - t * 40.0
        targets[1] = -45.0 + t * 35.0
        targets[2] = 90.0 - t * 50.0
        targets[3] = 25.0 - t * 20.0
        targets[6] = 20.0
        targets[7] = 70.0

    elif phase == "monitor":
        # Doctor returns to rest, nurse approaches patient
        targets[0] = 35.0 - t * 35.0
        targets[1] = -10.0 + t * 10.0
        targets[2] = 40.0 - t * 40.0
        targets[3] = 5.0 - t * 5.0
        # Nurse raises tablet to show patient
        targets[6] = 20.0 + t * 15.0
        targets[7] = 70.0 - t * 20.0

    # Convert degrees to radians for MuJoCo
    targets_rad = np.radians(targets)
    return targets_rad


def get_current_phase(elapsed: float) -> tuple[str, float]:
    """Determine the current phase and progress within it.

    Args:
        elapsed: Total elapsed simulation time in seconds.

    Returns:
        Tuple of (phase_name, normalized_progress [0, 1]).
    """
    phases = [
        ("prepare", PHASE_PREPARE),
        ("approach", PHASE_APPROACH),
        ("position", PHASE_POSITION),
        ("inject", PHASE_INJECT),
        ("hold", PHASE_HOLD),
        ("withdraw", PHASE_WITHDRAW),
        ("monitor", PHASE_MONITOR),
    ]

    cumulative = 0.0
    for name, duration in phases:
        if elapsed < cumulative + duration:
            progress = (elapsed - cumulative) / duration
            return name, float(np.clip(progress, 0.0, 1.0))
        cumulative += duration

    return "monitor", 1.0


def run_simulation(
    export_path: str | None = None,
    render: bool = False,
    fps: int = 30,
) -> dict:
    """Run the clinical injection simulation.

    Args:
        export_path: Optional file path to export animation data as JSON.
        render: Whether to render the simulation using MuJoCo viewer.
        fps: Frames per second for animation export.

    Returns:
        Dictionary containing simulation results and animation frames.
    """
    if not MODEL_PATH.exists():
        print(f"Error: Model file not found at {MODEL_PATH}")
        sys.exit(1)

    model = mujoco.MjModel.from_xml_path(str(MODEL_PATH))
    data = mujoco.MjData(model)

    # Reset simulation
    mujoco.mj_resetData(model, data)

    # Set initial patient pose (seated)
    joint_type = mujoco.mjtObj.mjOBJ_JOINT
    patient_hip_r = mujoco.mj_name2id(model, joint_type, "patient_r_hip_flex")
    patient_hip_l = mujoco.mj_name2id(model, joint_type, "patient_l_hip_flex")
    patient_knee_r = mujoco.mj_name2id(model, joint_type, "patient_r_knee_flex")
    patient_knee_l = mujoco.mj_name2id(model, joint_type, "patient_l_knee_flex")

    if patient_hip_r >= 0:
        data.qpos[model.jnt_qposadr[patient_hip_r]] = np.radians(-90)
    if patient_hip_l >= 0:
        data.qpos[model.jnt_qposadr[patient_hip_l]] = np.radians(-90)
    if patient_knee_r >= 0:
        data.qpos[model.jnt_qposadr[patient_knee_r]] = np.radians(-90)
    if patient_knee_l >= 0:
        data.qpos[model.jnt_qposadr[patient_knee_l]] = np.radians(-90)

    mujoco.mj_forward(model, data)

    # Animation data storage
    frames = []
    frame_interval = 1.0 / fps
    next_frame_time = 0.0
    steps = int(TOTAL_DURATION / model.opt.timestep)

    print(f"Running clinical injection simulation ({TOTAL_DURATION:.1f}s)...")
    print(f"Model: {model.nq} DOFs, {model.nu} actuators, {model.nbody} bodies")

    for step in range(steps):
        elapsed = step * model.opt.timestep
        phase, progress = get_current_phase(elapsed)

        # Compute and apply control targets
        targets = compute_injection_targets(model, progress, phase)
        data.ctrl[:] = targets

        # Step physics
        mujoco.mj_step(model, data)

        # Record frame at target FPS
        if elapsed >= next_frame_time:
            needle_pos = data.site_xpos[
                mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_SITE, "needle_tip")
            ].copy()
            target_pos = data.site_xpos[
                mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_SITE, "injection_target")
            ].copy()

            frame = {
                "time": round(elapsed, 4),
                "phase": phase,
                "progress": round(progress, 4),
                "qpos": data.qpos.copy().tolist(),
                "needle_pos": needle_pos.tolist(),
                "target_pos": target_pos.tolist(),
                "needle_target_dist": float(np.linalg.norm(needle_pos - target_pos)),
            }
            frames.append(frame)
            next_frame_time += frame_interval

    # Compute results
    min_dist = min(f["needle_target_dist"] for f in frames)
    inject_frames = [f for f in frames if f["phase"] == "inject"]
    avg_inject_dist = (
        np.mean([f["needle_target_dist"] for f in inject_frames])
        if inject_frames
        else float("inf")
    )

    results = {
        "model_name": "clinical_injection_sim",
        "duration": TOTAL_DURATION,
        "fps": fps,
        "total_frames": len(frames),
        "phases": [
            "prepare",
            "approach",
            "position",
            "inject",
            "hold",
            "withdraw",
            "monitor",
        ],
        "metrics": {
            "min_needle_target_distance": round(min_dist, 6),
            "avg_inject_distance": round(float(avg_inject_dist), 6),
        },
        "frames": frames,
    }

    print(f"Simulation complete: {len(frames)} frames captured")
    print(f"Min needle-target distance: {min_dist:.4f}m")
    print(f"Avg distance during injection: {avg_inject_dist:.4f}m")

    # Export if requested
    if export_path:
        output_file = Path(export_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        with open(output_file, "w") as f:
            json.dump(results, f, indent=2)
        print(f"Animation data exported to {output_file}")

    # Render if requested
    if render:
        try:
            with mujoco.viewer.launch_passive(model, data) as viewer:
                mujoco.mj_resetData(model, data)
                for step in range(steps):
                    elapsed = step * model.opt.timestep
                    phase, progress = get_current_phase(elapsed)
                    targets = compute_injection_targets(model, progress, phase)
                    data.ctrl[:] = targets
                    mujoco.mj_step(model, data)
                    viewer.sync()
        except Exception as e:
            print(f"Viewer not available: {e}")
            print("Run without --render or use the web viewer instead.")

    return results


def main() -> None:
    """Entry point for the clinical simulation."""
    parser = argparse.ArgumentParser(
        description="Clinical Injection Simulation with G1 Humanoid Robots"
    )
    parser.add_argument(
        "--export",
        type=str,
        default=None,
        help="Export animation data to JSON file",
    )
    parser.add_argument(
        "--render",
        action="store_true",
        help="Render simulation using MuJoCo viewer",
    )
    parser.add_argument(
        "--fps",
        type=int,
        default=30,
        help="Frames per second for animation export (default: 30)",
    )
    args = parser.parse_args()
    run_simulation(
        export_path=args.export,
        render=args.render,
        fps=args.fps,
    )


if __name__ == "__main__":
    main()
