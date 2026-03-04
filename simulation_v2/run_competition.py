"""Run the 4-station clinical competition simulation.

Simulates four doctor/patient/nurse stations competing simultaneously.
Each station uses a PPO-trained policy with different random seed
initialization, producing distinct behavior profiles.

Usage:
    python -m simulation_v2.run_competition
    python -m simulation_v2.run_competition --export output/competition.json
    python -m simulation_v2.run_competition --fps 60
"""

import argparse
import json
from pathlib import Path

from simulation_v2.constants import (
    STATION_CONFIGS,
    CompetitionResult,
    StationMetrics,
    validate_fps,
)
from simulation_v2.ppo_policy import (
    compute_injection_accuracy,
    compute_motion_smoothness,
    compute_phase_durations,
    compute_ppo_reward,
)


def run_station(station_idx: int) -> StationMetrics:
    """Run a single station's competition and compute metrics.

    Args:
        station_idx: Index into STATION_CONFIGS.

    Returns:
        Metrics for the station run.
    """
    config = STATION_CONFIGS[station_idx]
    doctor_phases, nurse_phases = compute_phase_durations(config)

    doctor_time = sum(d for _, d, _ in doctor_phases)
    nurse_time = sum(d for _, d, _ in nurse_phases)
    total_time = doctor_time + nurse_time

    accuracy_dist = compute_injection_accuracy(config)
    smoothness = compute_motion_smoothness(config)

    accuracy_score = 1.0 / (1.0 + accuracy_dist * 100.0)
    reward = compute_ppo_reward(total_time, accuracy_dist, smoothness)

    return {
        "station_id": config["id"],
        "doctor_review_time": round(doctor_time, 3),
        "nurse_injection_time": round(nurse_time, 3),
        "total_time": round(total_time, 3),
        "injection_accuracy": round(accuracy_score, 4),
        "needle_target_distance": round(accuracy_dist, 6),
        "ppo_reward": reward,
        "rank": 0,  # Computed after all stations finish
    }


def run_competition(
    export_path: str | None = None,
    fps: int = 30,
) -> CompetitionResult:
    """Run the full 4-station competition simulation.

    Args:
        export_path: Optional file path for JSON export.
        fps: Frames per second for animation export.

    Returns:
        Competition results with station rankings.
    """
    validate_fps(fps)

    print("=" * 60)
    print("  CLINICAL ROBOT COMPETITION — 4-Station PPO Simulation")
    print("=" * 60)
    print()

    stations: list[StationMetrics] = []
    for i in range(len(STATION_CONFIGS)):
        metrics = run_station(i)
        stations.append(metrics)
        print(f"Station {metrics['station_id']}:")
        print(f"  Doctor review:    {metrics['doctor_review_time']:.3f}s")
        print(f"  Nurse injection:  {metrics['nurse_injection_time']:.3f}s")
        print(f"  Total time:       {metrics['total_time']:.3f}s")
        print(f"  Accuracy score:   {metrics['injection_accuracy']:.4f}")
        print(f"  Needle distance:  {metrics['needle_target_distance']:.6f}m")
        print(f"  PPO reward:       {metrics['ppo_reward']:.4f}")
        print()

    # Rank by total time (lower is better), tiebreak by accuracy.
    ranked = sorted(
        stations,
        key=lambda s: (s["total_time"], -s["injection_accuracy"]),
    )
    for rank, station in enumerate(ranked, 1):
        station["rank"] = rank

    winner = ranked[0]["station_id"]
    print(f"  WINNER: Station {winner} ({ranked[0]['total_time']:.3f}s)")
    print()

    result: CompetitionResult = {
        "version": "0.8.0",
        "simulation": "clinical_competition",
        "num_stations": len(stations),
        "max_duration": max(s["total_time"] for s in stations),
        "fps": fps,
        "ppo_config": {
            "weight_time": -0.3,
            "weight_accuracy": 0.5,
            "weight_smooth": 0.2,
            "architecture": "MLP_64x64_tanh",
            "training_episodes": 500,
            "gamma": 0.99,
            "clip_ratio": 0.2,
            "learning_rate": 3e-4,
        },
        "stations": stations,
        "winner": winner,
    }

    if export_path:
        output_file = Path(export_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2)
        print(f"Results exported to {output_file}")

    return result


def main() -> None:
    """Entry point for the competition simulation."""
    parser = argparse.ArgumentParser(
        description="4-Station Clinical Robot Competition with PPO Policies"
    )
    parser.add_argument(
        "--export",
        type=str,
        default=None,
        help="Export competition results to JSON file",
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

    run_competition(export_path=args.export, fps=args.fps)


if __name__ == "__main__":
    main()
