"""Shared constants for the multi-station competition simulation (v0.2.0).

Defines phase timings, PPO reward parameters, station configurations,
and type-safe data structures for the 4-station clinical competition.
"""

from __future__ import annotations

from typing import TypedDict

# Minimum allowed FPS.
MIN_FPS = 1

# ── Doctor Review Phases ──────────────────────────────────────────────
DOCTOR_PHASES: list[tuple[str, float, str]] = [
    ("receive_chart", 1.0, "Receiving patient chart"),
    ("review_symptoms", 2.0, "Reviewing symptoms"),
    ("assess_toxicity", 1.5, "Assessing toxicity levels"),
    ("approve_injection", 1.0, "Approving injection"),
]

DOCTOR_DURATION = sum(d for _, d, _ in DOCTOR_PHASES)

# ── Nurse Injection Phases ────────────────────────────────────────────
NURSE_PHASES: list[tuple[str, float, str]] = [
    ("prepare_syringe", 1.0, "Preparing syringe"),
    ("approach_patient", 1.5, "Approaching patient"),
    ("position_needle", 1.5, "Positioning needle at deltoid"),
    ("inject", 2.0, "Administering medication"),
    ("hold_steady", 1.5, "Holding steady"),
    ("withdraw", 1.0, "Withdrawing needle"),
]

NURSE_DURATION = sum(d for _, d, _ in NURSE_PHASES)

# Total base simulation duration (doctor review + nurse injection).
TOTAL_BASE_DURATION = DOCTOR_DURATION + NURSE_DURATION  # 13.0s

# Maximum simulation time (with PPO variance overhead).
MAX_SIM_DURATION = 20.0

# ── Station Grid Layout ──────────────────────────────────────────────
NUM_STATIONS = 4
GRID_COLS = 2
GRID_ROWS = 2
GRID_SPACING_X = 4.5  # meters between station centers
GRID_SPACING_Z = 4.0  # meters between station rows

# Station positions in 2x2 grid (x, z offsets from room center).
STATION_POSITIONS: list[tuple[float, float]] = [
    (-GRID_SPACING_X / 2, -GRID_SPACING_Z / 2),  # Station A (front-left)
    (GRID_SPACING_X / 2, -GRID_SPACING_Z / 2),  # Station B (front-right)
    (-GRID_SPACING_X / 2, GRID_SPACING_Z / 2),  # Station C (back-left)
    (GRID_SPACING_X / 2, GRID_SPACING_Z / 2),  # Station D (back-right)
]

STATION_LABELS = ["A", "B", "C", "D"]

# ── PPO Reward Weights ───────────────────────────────────────────────
# R = w_time * R_time + w_accuracy * R_accuracy + w_smooth * R_smooth
PPO_WEIGHT_TIME = -0.3  # Penalty per second of elapsed time
PPO_WEIGHT_ACCURACY = 0.5  # Reward for injection accuracy (1/(1+dist))
PPO_WEIGHT_SMOOTH = 0.2  # Reward for smooth motion (1/(1+jerk))

# ── Per-Station PPO Configurations ───────────────────────────────────
# Each station has a unique random seed producing different learned
# policy parameters after simulated PPO training.


class StationConfig(TypedDict):
    """Configuration for a single competition station."""

    id: str
    seed: int
    speed_factor: float  # Multiplier on phase durations (<1 = faster)
    accuracy_bias: float  # Offset on needle targeting (lower = better)
    smoothness: float  # Motion smoothness parameter [0, 1]


STATION_CONFIGS: list[StationConfig] = [
    {
        "id": "A",
        "seed": 42,
        "speed_factor": 1.00,
        "accuracy_bias": 0.010,
        "smoothness": 0.85,
    },
    {
        "id": "B",
        "seed": 137,
        "speed_factor": 0.88,
        "accuracy_bias": 0.018,
        "smoothness": 0.72,
    },
    {
        "id": "C",
        "seed": 256,
        "speed_factor": 1.08,
        "accuracy_bias": 0.006,
        "smoothness": 0.92,
    },
    {
        "id": "D",
        "seed": 512,
        "speed_factor": 0.95,
        "accuracy_bias": 0.013,
        "smoothness": 0.80,
    },
]


# ── Type-Safe Data Structures ────────────────────────────────────────


class StationMetrics(TypedDict):
    """Metrics for a single station after competition."""

    station_id: str
    doctor_review_time: float
    nurse_injection_time: float
    total_time: float
    injection_accuracy: float  # 0-1 score (1 = perfect)
    needle_target_distance: float  # meters
    ppo_reward: float
    rank: int


class PpoConfig(TypedDict):
    """PPO policy configuration payload."""

    weight_time: float
    weight_accuracy: float
    weight_smooth: float
    architecture: str
    training_episodes: int
    gamma: float
    clip_ratio: float
    learning_rate: float


class CompetitionResult(TypedDict):
    """Full competition result payload."""

    version: str
    simulation: str
    num_stations: int
    max_duration: float
    fps: int
    ppo_config: PpoConfig
    stations: list[StationMetrics]
    winner: str


def validate_fps(fps: int) -> None:
    """Validate FPS parameter.

    Raises:
        ValueError: If fps is less than MIN_FPS.
    """
    if fps < MIN_FPS:
        msg = f"fps must be >= {MIN_FPS}, got {fps}"
        raise ValueError(msg)
