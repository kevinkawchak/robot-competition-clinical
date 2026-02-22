"""Export multi-station competition animation data for the web viewer.

Generates pre-computed keyframes for all 4 stations so the Three.js
competition viewer can replay the race without requiring MuJoCo.

Usage:
    python -m simulation_v2.export_competition
    python -m simulation_v2.export_competition --output docs/v2/competition_data.json
"""

import argparse
import json
import math
from pathlib import Path

from simulation_v2.constants import (
    STATION_CONFIGS,
    validate_fps,
)
from simulation_v2.ppo_policy import (
    compute_doctor_arm_targets,
    compute_injection_accuracy,
    compute_motion_smoothness,
    compute_nurse_arm_targets,
    compute_phase_durations,
    compute_ppo_reward,
)


def generate_station_animation(
    station_idx: int,
    fps: int = 30,
) -> dict:
    """Generate animation keyframes for a single station.

    Args:
        station_idx: Index into STATION_CONFIGS.
        fps: Target frames per second.

    Returns:
        Dictionary with station animation data and metrics.
    """
    config = STATION_CONFIGS[station_idx]
    doctor_phases, nurse_phases = compute_phase_durations(config)
    smoothness = compute_motion_smoothness(config)
    accuracy_dist = compute_injection_accuracy(config)

    doctor_time = sum(d for _, d, _ in doctor_phases)
    nurse_time = sum(d for _, d, _ in nurse_phases)
    total_time = doctor_time + nurse_time

    frame_dt = 1.0 / fps
    total_frames = math.ceil(total_time * fps)
    keyframes = []

    for i in range(total_frames + 1):
        time = min(i * frame_dt, total_time)
        is_doctor_phase = time < doctor_time

        if is_doctor_phase:
            # Doctor review phases
            elapsed = 0.0
            current_name = doctor_phases[-1][0]
            current_label = doctor_phases[-1][2]
            progress = 1.0
            for name, dur, label in doctor_phases:
                if time < elapsed + dur:
                    current_name = name
                    current_label = label
                    progress = (time - elapsed) / dur
                    break
                elapsed += dur

            doctor_arm = compute_doctor_arm_targets(current_name, progress)
            nurse_arm = {
                "shoulder_pitch": 0.0,
                "elbow": 0.0,
                "wrist": 0.0,
                "x_offset": 0.0,
            }
            role_active = "doctor"
        else:
            # Nurse injection phases
            nurse_elapsed = time - doctor_time
            elapsed = 0.0
            current_name = nurse_phases[-1][0]
            current_label = nurse_phases[-1][2]
            progress = 1.0
            for name, dur, label in nurse_phases:
                if nurse_elapsed < elapsed + dur:
                    current_name = name
                    current_label = label
                    progress = (nurse_elapsed - elapsed) / dur
                    break
                elapsed += dur

            nurse_arm = compute_nurse_arm_targets(current_name, progress, smoothness)
            doctor_arm = {"shoulder_pitch": 20.0, "elbow": 65.0}
            role_active = "nurse"

        keyframes.append(
            {
                "t": round(time, 3),
                "phase": current_name,
                "label": current_label,
                "role_active": role_active,
                "progress": round(max(0.0, min(1.0, progress)), 4),
                "doctor": doctor_arm,
                "nurse": nurse_arm,
            }
        )

    accuracy_score = 1.0 / (1.0 + accuracy_dist * 100.0)
    reward = compute_ppo_reward(total_time, accuracy_dist, smoothness)

    return {
        "station_id": config["id"],
        "seed": config["seed"],
        "doctor_time": round(doctor_time, 3),
        "nurse_time": round(nurse_time, 3),
        "total_time": round(total_time, 3),
        "accuracy_distance": round(accuracy_dist, 6),
        "accuracy_score": round(accuracy_score, 4),
        "smoothness": round(smoothness, 4),
        "ppo_reward": round(reward, 4),
        "total_frames": len(keyframes),
        "keyframes": keyframes,
    }


def generate_competition_animation(fps: int = 30) -> dict:
    """Generate animation data for all 4 competition stations.

    Args:
        fps: Target frames per second.

    Returns:
        Full competition animation payload.
    """
    stations = []
    for i in range(len(STATION_CONFIGS)):
        station_data = generate_station_animation(i, fps)
        stations.append(station_data)

    # Rank stations
    ranked = sorted(stations, key=lambda s: (s["total_time"], -s["accuracy_score"]))
    for rank, station in enumerate(ranked, 1):
        station["rank"] = rank

    return {
        "version": "0.5.0",
        "simulation": "clinical_competition",
        "description": (
            "4-station clinical robot competition. Each station has a "
            "doctor (white coat, left) reviewing symptoms/toxicities and "
            "a nurse (blue coat, right) performing deltoid IM injection. "
            "PPO-trained policies with different seeds produce distinct "
            "behavior profiles for each station."
        ),
        "attribution": "Simulation framework inspired by mjlab (mujocolab/mjlab)",
        "num_stations": len(stations),
        "fps": fps,
        "ppo_config": {
            "architecture": "MLP_64x64_tanh",
            "observation_space": [
                "phase_progress",
                "arm_joint_angles",
                "needle_pos",
                "target_pos",
                "elapsed_time",
            ],
            "action_space": [
                "shoulder_pitch_delta",
                "elbow_delta",
                "wrist_delta",
                "approach_velocity",
            ],
            "reward_weights": {
                "time": -0.3,
                "accuracy": 0.5,
                "smoothness": 0.2,
            },
            "training_episodes": 500,
            "gamma": 0.99,
            "clip_ratio": 0.2,
            "learning_rate": 3e-4,
        },
        "stations": stations,
        "winner": ranked[0]["station_id"],
    }


def main() -> None:
    """Generate and export competition animation data."""
    parser = argparse.ArgumentParser(
        description="Export competition animation for web viewer"
    )
    parser.add_argument(
        "--output",
        type=str,
        default="docs/v2/competition_data.json",
        help="Output JSON file path",
    )
    parser.add_argument(
        "--fps",
        type=int,
        default=30,
        help="Frames per second (default: 30)",
    )
    args = parser.parse_args()

    try:
        validate_fps(args.fps)
    except ValueError as e:
        parser.error(str(e))

    animation = generate_competition_animation(fps=args.fps)

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(animation, f, separators=(",", ":"))

    size_kb = output_path.stat().st_size / 1024
    print(f"Exported {len(animation['stations'])} stations to {output_path}")
    print(f"File size: {size_kb:.1f} KB")
    for s in animation["stations"]:
        print(
            f"  Station {s['station_id']}: "
            f"{s['total_frames']} frames, "
            f"{s['total_time']:.3f}s, "
            f"rank #{s.get('rank', '?')}"
        )


if __name__ == "__main__":
    main()
