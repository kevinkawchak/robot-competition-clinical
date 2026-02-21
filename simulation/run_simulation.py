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
import math
import sys
from pathlib import Path

import mujoco
import numpy as np

from simulation.constants import (
    TOTAL_DURATION,
    FrameData,
    SimulationResult,
    get_current_phase,
    validate_fps,
)

# Scene model path relative to this file
MODEL_PATH = Path(__file__).parent / "models" / "clinical_scene.xml"


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
        Array of actuator control targets (radians).
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
        targets[0] = t * 30.0
        targets[2] = t * 60.0
        targets[3] = t * 10.0
        targets[6] = t * 20.0
        targets[7] = t * 70.0

    elif phase == "approach":
        targets[0] = 30.0 + t * 40.0
        targets[1] = t * (-30.0)
        targets[2] = 60.0 + t * 20.0
        targets[3] = 10.0 + t * 15.0
        targets[6] = 20.0
        targets[7] = 70.0

    elif phase == "position":
        targets[0] = 70.0 + t * 5.0
        targets[1] = -30.0 - t * 10.0
        targets[2] = 80.0 + t * 10.0
        targets[3] = 25.0 + t * 5.0
        targets[6] = 20.0
        targets[7] = 70.0

    elif phase == "inject":
        targets[0] = 75.0
        targets[1] = -40.0 - t * 5.0
        targets[2] = 90.0
        targets[3] = 30.0 - t * 5.0
        targets[6] = 20.0
        targets[7] = 70.0

    elif phase == "hold":
        targets[0] = 75.0
        targets[1] = -45.0
        targets[2] = 90.0
        targets[3] = 25.0
        targets[6] = 20.0
        targets[7] = 70.0

    elif phase == "withdraw":
        targets[0] = 75.0 - t * 40.0
        targets[1] = -45.0 + t * 35.0
        targets[2] = 90.0 - t * 50.0
        targets[3] = 25.0 - t * 20.0
        targets[6] = 20.0
        targets[7] = 70.0

    elif phase == "monitor":
        targets[0] = 35.0 - t * 35.0
        targets[1] = -10.0 + t * 10.0
        targets[2] = 40.0 - t * 40.0
        targets[3] = 5.0 - t * 5.0
        targets[6] = 20.0 + t * 15.0
        targets[7] = 70.0 - t * 20.0

    targets_rad = np.radians(targets)
    return targets_rad


def _resolve_site_id(model: mujoco.MjModel, name: str) -> int:
    """Resolve a MuJoCo site ID, failing fast if not found.

    Args:
        model: MuJoCo model instance.
        name: Site name to look up.

    Returns:
        Non-negative site ID.

    Raises:
        RuntimeError: If the site name is not found in the model.
    """
    site_id = mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_SITE, name)
    if site_id < 0:
        msg = f"Site '{name}' not found in model"
        raise RuntimeError(msg)
    return site_id


def run_simulation(
    export_path: str | None = None,
    render: bool = False,
    fps: int = 30,
) -> SimulationResult:
    """Run the clinical injection simulation.

    Args:
        export_path: Optional file path to export animation data as JSON.
        render: Whether to render the simulation using MuJoCo viewer.
        fps: Frames per second for animation export.

    Returns:
        Dictionary containing simulation results and animation frames.

    Raises:
        ValueError: If fps is less than 1.
        RuntimeError: If required sites are missing from the model.
    """
    validate_fps(fps)

    if not MODEL_PATH.exists():
        print(f"Error: Model file not found at {MODEL_PATH}")
        sys.exit(1)

    model = mujoco.MjModel.from_xml_path(str(MODEL_PATH))
    data = mujoco.MjData(model)

    # Resolve site IDs once before the simulation loop (peer review #2, #5).
    needle_site_id = _resolve_site_id(model, "needle_tip")
    target_site_id = _resolve_site_id(model, "injection_target")

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
    frames: list[FrameData] = []
    frame_interval = 1.0 / fps
    next_frame_time = 0.0

    # Use math.ceil to include the final fractional step (peer review #3).
    steps = math.ceil(TOTAL_DURATION / model.opt.timestep)

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

        # Record frame at target FPS using precomputed site IDs.
        if elapsed >= next_frame_time:
            needle_pos = data.site_xpos[needle_site_id].copy()
            target_pos = data.site_xpos[target_site_id].copy()

            frame: FrameData = {
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

    # Capture explicit final frame at TOTAL_DURATION (peer review #3).
    if not frames or frames[-1]["time"] < TOTAL_DURATION - frame_interval:
        phase, progress = get_current_phase(TOTAL_DURATION)
        needle_pos = data.site_xpos[needle_site_id].copy()
        target_pos = data.site_xpos[target_site_id].copy()
        final_frame: FrameData = {
            "time": round(TOTAL_DURATION, 4),
            "phase": phase,
            "progress": 1.0,
            "qpos": data.qpos.copy().tolist(),
            "needle_pos": needle_pos.tolist(),
            "target_pos": target_pos.tolist(),
            "needle_target_dist": float(np.linalg.norm(needle_pos - target_pos)),
        }
        frames.append(final_frame)

    # Compute results
    min_dist = min(f["needle_target_dist"] for f in frames)
    inject_frames = [f for f in frames if f["phase"] == "inject"]
    avg_inject_dist = (
        float(np.mean([f["needle_target_dist"] for f in inject_frames]))
        if inject_frames
        else float("inf")
    )

    results: SimulationResult = {
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
            "avg_inject_distance": round(avg_inject_dist, 6),
        },
        "frames": frames,
    }

    print(f"Simulation complete: {len(frames)} frames captured")
    print(f"Min needle-target distance: {min_dist:.4f}m")
    print(f"Avg distance during injection: {avg_inject_dist:.4f}m")

    # Export if requested (peer review #7: explicit encoding).
    if export_path:
        output_file = Path(export_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2)
        print(f"Animation data exported to {output_file}")

    # Render if requested (peer review #4: narrow exception handling).
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
        except (ImportError, AttributeError) as e:
            print(f"Viewer not available (missing display backend): {e}")
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

    try:
        validate_fps(args.fps)
    except ValueError as e:
        parser.error(str(e))

    run_simulation(
        export_path=args.export,
        render=args.render,
        fps=args.fps,
    )


if __name__ == "__main__":
    main()
