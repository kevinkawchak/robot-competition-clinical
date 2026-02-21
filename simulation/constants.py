"""Shared constants for the clinical injection simulation.

Centralizes phase timing and configuration values used by both
the MuJoCo simulation runner and the web animation exporter.
"""

from __future__ import annotations

from typing import TypedDict

# Minimum allowed FPS for animation export and simulation capture.
MIN_FPS = 1

# Injection procedure phase timings (seconds).
PHASE_TIMINGS: list[tuple[str, float, str]] = [
    ("prepare", 1.0, "Preparing syringe"),
    ("approach", 2.0, "Approaching patient"),
    ("position", 1.5, "Positioning at deltoid"),
    ("inject", 2.0, "Administering medication"),
    ("hold", 1.5, "Holding steady"),
    ("withdraw", 1.5, "Withdrawing syringe"),
    ("monitor", 2.0, "Post-injection monitoring"),
]

# Individual phase durations for backward-compatible references.
PHASE_PREPARE = 1.0
PHASE_APPROACH = 2.0
PHASE_POSITION = 1.5
PHASE_INJECT = 2.0
PHASE_HOLD = 1.5
PHASE_WITHDRAW = 1.5
PHASE_MONITOR = 2.0

TOTAL_DURATION = sum(duration for _, duration, _ in PHASE_TIMINGS)

PHASE_NAMES = [name for name, _, _ in PHASE_TIMINGS]


class FrameData(TypedDict):
    """Type-safe structure for a single simulation frame."""

    time: float
    phase: str
    progress: float
    qpos: list[float]
    needle_pos: list[float]
    target_pos: list[float]
    needle_target_dist: float


class SimulationMetrics(TypedDict):
    """Type-safe structure for simulation result metrics."""

    min_needle_target_distance: float
    avg_inject_distance: float


class SimulationResult(TypedDict):
    """Type-safe structure for the full simulation result payload."""

    model_name: str
    duration: float
    fps: int
    total_frames: int
    phases: list[str]
    metrics: SimulationMetrics
    frames: list[FrameData]


class AnimationKeyframe(TypedDict):
    """Type-safe structure for a web animation keyframe."""

    t: float
    phase: str
    label: str
    doctor: dict[str, float]
    nurse: dict[str, float]


class AnimationData(TypedDict):
    """Type-safe structure for the full web animation payload."""

    version: str
    simulation: str
    description: str
    attribution: str
    duration: float
    fps: int
    total_frames: int
    phases: list[dict[str, object]]
    keyframes: list[AnimationKeyframe]


def validate_fps(fps: int) -> None:
    """Validate FPS parameter, raising ValueError if invalid.

    Args:
        fps: Frames per second value to validate.

    Raises:
        ValueError: If fps is less than MIN_FPS.
    """
    if fps < MIN_FPS:
        msg = f"fps must be >= {MIN_FPS}, got {fps}"
        raise ValueError(msg)


def get_current_phase(elapsed: float) -> tuple[str, float]:
    """Determine the current phase and progress within it.

    Args:
        elapsed: Total elapsed simulation time in seconds.

    Returns:
        Tuple of (phase_name, normalized_progress [0, 1]).
    """
    cumulative = 0.0
    for name, duration, _ in PHASE_TIMINGS:
        if elapsed < cumulative + duration:
            progress = (elapsed - cumulative) / duration
            return name, max(0.0, min(1.0, progress))
        cumulative += duration
    return "monitor", 1.0
