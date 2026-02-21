"""Unit tests for phase transitions in the clinical simulation."""

from __future__ import annotations

import pytest

from simulation.constants import (
    TOTAL_DURATION,
    get_current_phase,
)
from simulation_v2.constants import STATION_CONFIGS
from simulation_v2.ppo_policy import compute_phase_durations

# ── get_current_phase returns correct phase names at various times ───


class TestGetCurrentPhase:
    """Tests for simulation.constants.get_current_phase."""

    def test_phase_at_time_zero(self) -> None:
        """Phase at t=0.0 is 'prepare'."""
        phase, progress = get_current_phase(0.0)
        assert phase == "prepare"

    def test_phase_at_time_half_second(self) -> None:
        """Phase at t=0.5 is still 'prepare' (duration=1.0)."""
        phase, _ = get_current_phase(0.5)
        assert phase == "prepare"

    def test_phase_at_time_1_0(self) -> None:
        """Phase at t=1.0 transitions to 'approach'."""
        phase, _ = get_current_phase(1.0)
        assert phase == "approach"

    def test_phase_at_time_3_0(self) -> None:
        """Phase at t=3.0 transitions to 'position'."""
        phase, _ = get_current_phase(3.0)
        assert phase == "position"

    def test_phase_at_time_4_5(self) -> None:
        """Phase at t=4.5 transitions to 'inject'."""
        phase, _ = get_current_phase(4.5)
        assert phase == "inject"

    def test_phase_at_time_6_5(self) -> None:
        """Phase at t=6.5 transitions to 'hold'."""
        phase, _ = get_current_phase(6.5)
        assert phase == "hold"

    def test_phase_at_time_8_0(self) -> None:
        """Phase at t=8.0 transitions to 'withdraw'."""
        phase, _ = get_current_phase(8.0)
        assert phase == "withdraw"

    def test_phase_at_time_9_5(self) -> None:
        """Phase at t=9.5 transitions to 'monitor'."""
        phase, _ = get_current_phase(9.5)
        assert phase == "monitor"

    def test_phase_at_time_11_5(self) -> None:
        """Phase at t=11.5 (past TOTAL_DURATION) returns 'monitor'."""
        phase, _ = get_current_phase(11.5)
        assert phase == "monitor"


# ── Phase boundaries ────────────────────────────────────────────────


class TestPhaseBoundaries:
    """Tests that phase boundaries are computed correctly."""

    @pytest.mark.parametrize(
        ("time", "expected_phase"),
        [
            (0.0, "prepare"),
            (1.0, "approach"),
            (3.0, "position"),
            (4.5, "inject"),
            (6.5, "hold"),
            (8.0, "withdraw"),
            (9.5, "monitor"),
            (11.5, "monitor"),
        ],
    )
    def test_boundary_phases(self, time: float, expected_phase: str) -> None:
        """Phase at each boundary time matches the expected name."""
        phase, _ = get_current_phase(time)
        assert phase == expected_phase


# ── Progress is always in [0, 1] ────────────────────────────────────


class TestProgressRange:
    """Tests that progress values are always clamped to [0, 1]."""

    @pytest.mark.parametrize("time", [0.0, 0.5, 1.0, 3.5, 6.0, 9.0, 11.5])
    def test_progress_in_unit_interval(self, time: float) -> None:
        """Progress at any given time is between 0.0 and 1.0 inclusive."""
        _, progress = get_current_phase(time)
        assert 0.0 <= progress <= 1.0

    def test_progress_at_start_is_zero(self) -> None:
        """Progress at t=0.0 should be 0.0."""
        _, progress = get_current_phase(0.0)
        assert progress == 0.0

    def test_progress_negative_time(self) -> None:
        """Progress at negative time is clamped to 0.0."""
        _, progress = get_current_phase(-1.0)
        assert 0.0 <= progress <= 1.0


# ── Final phase ─────────────────────────────────────────────────────


class TestFinalPhase:
    """Tests that the final phase at TOTAL_DURATION is 'monitor'."""

    def test_final_phase_name(self) -> None:
        """At TOTAL_DURATION the phase is 'monitor'."""
        phase, _ = get_current_phase(TOTAL_DURATION)
        assert phase == "monitor"

    def test_final_phase_progress(self) -> None:
        """At TOTAL_DURATION progress is 1.0."""
        _, progress = get_current_phase(TOTAL_DURATION)
        assert progress == 1.0

    def test_beyond_total_duration(self) -> None:
        """Beyond TOTAL_DURATION the phase remains 'monitor' with progress 1.0."""
        phase, progress = get_current_phase(TOTAL_DURATION + 100.0)
        assert phase == "monitor"
        assert progress == 1.0


# ── compute_phase_durations returns valid durations ─────────────────


class TestComputePhaseDurations:
    """Tests for simulation_v2.ppo_policy.compute_phase_durations."""

    def test_returns_doctor_and_nurse_phases(self) -> None:
        """compute_phase_durations returns a 2-tuple of lists."""
        config = STATION_CONFIGS[0]
        doctor, nurse = compute_phase_durations(config)
        assert isinstance(doctor, list)
        assert isinstance(nurse, list)

    def test_doctor_phases_count(self) -> None:
        """Doctor phases list has the expected number of entries."""
        config = STATION_CONFIGS[0]
        doctor, _ = compute_phase_durations(config)
        assert len(doctor) == 4

    def test_nurse_phases_count(self) -> None:
        """Nurse phases list has the expected number of entries."""
        config = STATION_CONFIGS[0]
        _, nurse = compute_phase_durations(config)
        assert len(nurse) == 6

    @pytest.mark.parametrize("station_idx", range(4))
    def test_all_durations_positive(self, station_idx: int) -> None:
        """All phase durations are positive for every station."""
        config = STATION_CONFIGS[station_idx]
        doctor, nurse = compute_phase_durations(config)
        for _, dur, _ in doctor:
            assert dur > 0.0
        for _, dur, _ in nurse:
            assert dur > 0.0

    @pytest.mark.parametrize("station_idx", range(4))
    def test_all_durations_at_least_0_3(self, station_idx: int) -> None:
        """All durations are >= 0.3 seconds (the enforced floor)."""
        config = STATION_CONFIGS[station_idx]
        doctor, nurse = compute_phase_durations(config)
        for _, dur, _ in doctor:
            assert dur >= 0.3, f"Doctor phase duration {dur} is below 0.3"
        for _, dur, _ in nurse:
            assert dur >= 0.3, f"Nurse phase duration {dur} is below 0.3"

    def test_deterministic_with_same_config(self) -> None:
        """Calling with the same config produces identical results."""
        config = STATION_CONFIGS[0]
        result_a = compute_phase_durations(config)
        result_b = compute_phase_durations(config)
        assert result_a == result_b

    def test_phase_tuples_have_three_elements(self) -> None:
        """Each phase tuple contains (name, duration, label)."""
        config = STATION_CONFIGS[0]
        doctor, nurse = compute_phase_durations(config)
        for entry in doctor + nurse:
            assert len(entry) == 3
            name, dur, label = entry
            assert isinstance(name, str)
            assert isinstance(dur, float)
            assert isinstance(label, str)
