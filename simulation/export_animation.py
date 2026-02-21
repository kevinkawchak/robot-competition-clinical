"""Export clinical simulation animation data for the web viewer.

Generates a self-contained JSON file that the Three.js web viewer
can load to replay the injection procedure animation.

Usage:
    python -m simulation.export_animation
    python -m simulation.export_animation --output docs/animation_data.json
"""

import argparse
import json
import math
from pathlib import Path

from simulation.constants import (
    PHASE_TIMINGS,
    TOTAL_DURATION,
    AnimationData,
    AnimationKeyframe,
    validate_fps,
)


def smooth_step(t: float) -> float:
    """Hermite smoothstep interpolation."""
    t = max(0.0, min(1.0, t))
    return t * t * (3.0 - 2.0 * t)


def generate_web_animation(fps: int = 30) -> AnimationData:
    """Generate animation keyframes for the web viewer.

    This creates pre-computed animation data that the Three.js viewer
    can use to animate the clinical injection procedure without requiring
    MuJoCo on the client device.

    Args:
        fps: Target frames per second.

    Returns:
        Dictionary with animation keyframes and metadata.

    Raises:
        ValueError: If fps is less than 1.
    """
    validate_fps(fps)

    phases = [
        {"name": name, "duration": duration, "label": label}
        for name, duration, label in PHASE_TIMINGS
    ]

    total_frames = math.ceil(TOTAL_DURATION * fps)
    frame_dt = 1.0 / fps

    keyframes: list[AnimationKeyframe] = []

    for i in range(total_frames):
        time = i * frame_dt
        elapsed = 0.0
        current_phase = phases[-1]
        phase_progress = 1.0

        for phase in phases:
            if time < elapsed + phase["duration"]:
                current_phase = phase
                phase_progress = (time - elapsed) / phase["duration"]
                break
            elapsed += phase["duration"]

        t = smooth_step(phase_progress)
        phase_name = current_phase["name"]

        # Doctor arm angles (degrees)
        doc_shoulder_pitch = 0.0
        doc_shoulder_yaw = 0.0
        doc_elbow = 0.0
        doc_wrist = 0.0

        # Nurse arm angles
        nurse_shoulder = 20.0
        nurse_elbow = 70.0

        # Doctor position offset (for walk animation)
        doc_x_offset = 0.0

        if phase_name == "prepare":
            doc_shoulder_pitch = t * 30.0
            doc_elbow = t * 60.0
            doc_wrist = t * 10.0

        elif phase_name == "approach":
            doc_shoulder_pitch = 30.0 + t * 40.0
            doc_shoulder_yaw = t * (-30.0)
            doc_elbow = 60.0 + t * 20.0
            doc_wrist = 10.0 + t * 15.0
            doc_x_offset = t * (-0.15)

        elif phase_name == "position":
            doc_shoulder_pitch = 70.0 + t * 5.0
            doc_shoulder_yaw = -30.0 - t * 10.0
            doc_elbow = 80.0 + t * 10.0
            doc_wrist = 25.0 + t * 5.0
            doc_x_offset = -0.15

        elif phase_name == "inject":
            doc_shoulder_pitch = 75.0
            doc_shoulder_yaw = -40.0 - t * 5.0
            doc_elbow = 90.0
            doc_wrist = 30.0 - t * 5.0
            doc_x_offset = -0.15

        elif phase_name == "hold":
            doc_shoulder_pitch = 75.0
            doc_shoulder_yaw = -45.0
            doc_elbow = 90.0
            doc_wrist = 25.0
            doc_x_offset = -0.15
            doc_shoulder_pitch += math.sin(time * 2.0) * 0.5

        elif phase_name == "withdraw":
            doc_shoulder_pitch = 75.0 - t * 40.0
            doc_shoulder_yaw = -45.0 + t * 35.0
            doc_elbow = 90.0 - t * 50.0
            doc_wrist = 25.0 - t * 20.0
            doc_x_offset = -0.15 + t * 0.15

        elif phase_name == "monitor":
            doc_shoulder_pitch = 35.0 - t * 35.0
            doc_shoulder_yaw = -10.0 + t * 10.0
            doc_elbow = 40.0 - t * 40.0
            doc_wrist = 5.0 - t * 5.0
            nurse_shoulder = 20.0 + t * 15.0
            nurse_elbow = 70.0 - t * 20.0

        keyframe: AnimationKeyframe = {
            "t": round(time, 3),
            "phase": phase_name,
            "label": current_phase["label"],
            "doctor": {
                "x_offset": round(doc_x_offset, 4),
                "r_shoulder_pitch": round(doc_shoulder_pitch, 2),
                "r_shoulder_yaw": round(doc_shoulder_yaw, 2),
                "r_elbow": round(doc_elbow, 2),
                "r_wrist": round(doc_wrist, 2),
            },
            "nurse": {
                "r_shoulder": round(nurse_shoulder, 2),
                "r_elbow": round(nurse_elbow, 2),
            },
        }
        keyframes.append(keyframe)

    return {
        "version": "1.0.0",
        "simulation": "clinical_injection",
        "description": (
            "G1 humanoid robot injection procedure animation data. "
            "Cancer medication delivery to patient deltoid (upper arm)."
        ),
        "attribution": "Simulation framework inspired by mjlab (mujocolab/mjlab)",
        "duration": TOTAL_DURATION,
        "fps": fps,
        "total_frames": len(keyframes),
        "phases": phases,
        "keyframes": keyframes,
    }


def main() -> None:
    """Generate and export animation data."""
    parser = argparse.ArgumentParser(
        description="Export clinical simulation animation for web viewer"
    )
    parser.add_argument(
        "--output",
        type=str,
        default="docs/animation_data.json",
        help="Output JSON file path (default: docs/animation_data.json)",
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

    animation = generate_web_animation(fps=args.fps)

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(animation, f, separators=(",", ":"))

    size_kb = output_path.stat().st_size / 1024
    print(f"Exported {animation['total_frames']} frames to {output_path}")
    print(f"File size: {size_kb:.1f} KB")
    print(f"Duration: {animation['duration']:.1f}s at {animation['fps']} FPS")


if __name__ == "__main__":
    main()
