"""PPO policy simulation for the multi-station clinical competition.

Each station's nurse agent is controlled by a PPO-trained policy that
determines movement timing, injection accuracy, and motion smoothness.
Policies share the same architecture but have different learned weights
due to different random seed initialization during training.

PPO Training Details (simulated):
    - Architecture: 2-layer MLP (64 hidden units each) with tanh activation
    - Observation space: [phase_progress, arm_joint_angles, needle_pos,
      target_pos, elapsed_time]
    - Action space: [shoulder_pitch_delta, elbow_delta, wrist_delta,
      approach_velocity]
    - Reward: R = -0.3 * elapsed_time + 0.5 / (1 + needle_dist)
              + 0.2 / (1 + motion_jerk)
    - Training: 500 episodes, gamma=0.99, clip_ratio=0.2, lr=3e-4
    - All 4 stations trained with the same hyperparameters but different
      random seeds, producing distinct but competent policies.
"""

from __future__ import annotations

import hashlib
import math

from simulation_v2.constants import (
    DOCTOR_PHASES,
    NURSE_PHASES,
    PPO_WEIGHT_ACCURACY,
    PPO_WEIGHT_SMOOTH,
    PPO_WEIGHT_TIME,
    StationConfig,
)


def _seeded_random(seed: int, index: int) -> float:
    """Deterministic pseudo-random float in [0, 1) from seed and index.

    Uses a hash-based approach for reproducibility without mutable state.
    """
    data = f"{seed}:{index}".encode()
    digest = hashlib.sha256(data).hexdigest()
    return int(digest[:8], 16) / 0xFFFFFFFF


def compute_phase_durations(
    config: StationConfig,
) -> tuple[list[tuple[str, float, str]], list[tuple[str, float, str]]]:
    """Compute PPO-modulated phase durations for a station.

    Each phase base duration is scaled by the station's speed_factor
    plus a small per-phase random perturbation derived from the seed.

    Args:
        config: Station configuration with seed and speed factor.

    Returns:
        Tuple of (doctor_phases, nurse_phases) with adjusted durations.
    """
    seed = config["seed"]
    sf = config["speed_factor"]

    doctor = []
    for i, (name, base_dur, label) in enumerate(DOCTOR_PHASES):
        noise = (_seeded_random(seed, i) - 0.5) * 0.2
        duration = round(base_dur * sf * (1.0 + noise), 3)
        duration = max(0.3, duration)  # Floor at 0.3s
        doctor.append((name, duration, label))

    nurse = []
    for i, (name, base_dur, label) in enumerate(NURSE_PHASES):
        noise = (_seeded_random(seed, 100 + i) - 0.5) * 0.2
        duration = round(base_dur * sf * (1.0 + noise), 3)
        duration = max(0.3, duration)  # Floor at 0.3s
        nurse.append((name, duration, label))

    return doctor, nurse


def compute_injection_accuracy(config: StationConfig) -> float:
    """Compute the needle-to-target distance for a station's injection.

    Lower accuracy_bias yields smaller distance (better accuracy).
    A per-seed random component adds realistic variation.

    Args:
        config: Station configuration.

    Returns:
        Simulated needle-target distance in meters.
    """
    base = config["accuracy_bias"]
    noise = (_seeded_random(config["seed"], 200) - 0.5) * 0.008
    return max(0.001, base + noise)


def compute_motion_smoothness(config: StationConfig) -> float:
    """Compute motion smoothness score for a station.

    Higher smoothness parameter yields a score closer to 1.0.

    Args:
        config: Station configuration.

    Returns:
        Smoothness score in [0, 1].
    """
    base = config["smoothness"]
    noise = (_seeded_random(config["seed"], 300) - 0.5) * 0.1
    return max(0.0, min(1.0, base + noise))


def compute_ppo_reward(
    total_time: float,
    accuracy_distance: float,
    smoothness: float,
) -> float:
    """Compute the PPO reward for a completed station run.

    R = w_time * total_time + w_accuracy / (1 + dist) + w_smooth / (1 + jerk)

    Args:
        total_time: Total elapsed time in seconds.
        accuracy_distance: Needle-to-target distance in meters.
        smoothness: Motion smoothness score [0, 1].

    Returns:
        Scalar PPO reward value.
    """
    r_time = PPO_WEIGHT_TIME * total_time
    r_accuracy = PPO_WEIGHT_ACCURACY / (1.0 + accuracy_distance)
    jerk = 1.0 - smoothness
    r_smooth = PPO_WEIGHT_SMOOTH / (1.0 + jerk)
    return round(r_time + r_accuracy + r_smooth, 4)


def smooth_interp(t: float) -> float:
    """Smoothstep interpolation for natural motion."""
    t = max(0.0, min(1.0, t))
    return t * t * (3.0 - 2.0 * t)


def compute_nurse_arm_targets(
    phase_name: str,
    phase_progress: float,
    smoothness: float,
) -> dict[str, float]:
    """Compute nurse arm joint angles for the current injection phase.

    Returns angles in degrees for the nurse's injection arm.

    Args:
        phase_name: Current nurse phase name.
        phase_progress: Normalized progress within the phase [0, 1].
        smoothness: Motion smoothness parameter affecting interpolation.

    Returns:
        Dictionary of joint name to angle (degrees).
    """
    blend = smooth_interp(phase_progress) * smoothness + phase_progress * (
        1.0 - smoothness
    )
    t = max(0.0, min(1.0, blend))

    shoulder_pitch = 0.0
    elbow = 0.0
    wrist = 0.0
    x_offset = 0.0

    if phase_name == "prepare_syringe":
        shoulder_pitch = t * 25.0
        elbow = t * 55.0
        wrist = t * 8.0
    elif phase_name == "approach_patient":
        shoulder_pitch = 25.0 + t * 45.0
        elbow = 55.0 + t * 25.0
        wrist = 8.0 + t * 12.0
        x_offset = t * (-0.12)
    elif phase_name == "position_needle":
        shoulder_pitch = 70.0 + t * 5.0
        elbow = 80.0 + t * 10.0
        wrist = 20.0 + t * 10.0
        x_offset = -0.12
    elif phase_name == "inject":
        shoulder_pitch = 75.0
        elbow = 90.0
        wrist = 30.0 - t * 5.0
        x_offset = -0.12
    elif phase_name == "hold_steady":
        shoulder_pitch = 75.0 + math.sin(phase_progress * math.pi * 2) * 0.3
        elbow = 90.0
        wrist = 25.0
        x_offset = -0.12
    elif phase_name == "withdraw":
        shoulder_pitch = 75.0 - t * 50.0
        elbow = 90.0 - t * 55.0
        wrist = 25.0 - t * 20.0
        x_offset = -0.12 + t * 0.12

    return {
        "shoulder_pitch": round(shoulder_pitch, 2),
        "elbow": round(elbow, 2),
        "wrist": round(wrist, 2),
        "x_offset": round(x_offset, 4),
    }


def compute_doctor_arm_targets(
    phase_name: str,
    phase_progress: float,
) -> dict[str, float]:
    """Compute doctor arm joint angles for the review phases.

    The doctor holds a tablet and gestures during symptom review.

    Args:
        phase_name: Current doctor phase name.
        phase_progress: Normalized progress within the phase [0, 1].

    Returns:
        Dictionary of joint name to angle (degrees).
    """
    t = smooth_interp(phase_progress)

    shoulder_pitch = 20.0
    elbow = 65.0

    if phase_name == "receive_chart":
        shoulder_pitch = t * 20.0
        elbow = t * 65.0
    elif phase_name == "review_symptoms":
        shoulder_pitch = 20.0 + t * 10.0
        elbow = 65.0 + t * 5.0
    elif phase_name == "assess_toxicity":
        shoulder_pitch = 30.0 + math.sin(phase_progress * math.pi) * 5.0
        elbow = 70.0
    elif phase_name == "approve_injection":
        shoulder_pitch = 30.0 - t * 10.0
        elbow = 70.0 - t * 5.0

    return {
        "shoulder_pitch": round(shoulder_pitch, 2),
        "elbow": round(elbow, 2),
    }
