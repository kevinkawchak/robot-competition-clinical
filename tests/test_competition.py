"""Unit tests for the multi-station competition simulation."""

from __future__ import annotations

import math

import pytest

from simulation_v2.constants import STATION_CONFIGS
from simulation_v2.run_competition import run_competition, run_station

# ── run_station returns valid StationMetrics ─────────────────────────


class TestRunStation:
    """Tests for simulation_v2.run_competition.run_station."""

    @pytest.mark.parametrize("idx", range(4))
    def test_returns_valid_station_metrics(self, idx: int) -> None:
        """run_station returns a dict with all required StationMetrics keys."""
        metrics = run_station(idx)
        required_keys = {
            "station_id",
            "doctor_review_time",
            "nurse_injection_time",
            "total_time",
            "injection_accuracy",
            "needle_target_distance",
            "ppo_reward",
            "rank",
        }
        assert required_keys.issubset(metrics.keys())

    @pytest.mark.parametrize("idx", range(4))
    def test_station_id_matches_config(self, idx: int) -> None:
        """station_id matches the configured station ID."""
        metrics = run_station(idx)
        assert metrics["station_id"] == STATION_CONFIGS[idx]["id"]

    @pytest.mark.parametrize("idx", range(4))
    def test_total_time_is_sum_of_parts(self, idx: int) -> None:
        """total_time equals doctor_review_time + nurse_injection_time."""
        metrics = run_station(idx)
        expected = metrics["doctor_review_time"] + metrics["nurse_injection_time"]
        assert metrics["total_time"] == pytest.approx(expected, abs=0.01)

    @pytest.mark.parametrize("idx", range(4))
    def test_times_are_positive(self, idx: int) -> None:
        """All time values are positive."""
        metrics = run_station(idx)
        assert metrics["doctor_review_time"] > 0.0
        assert metrics["nurse_injection_time"] > 0.0
        assert metrics["total_time"] > 0.0


# ── All 4 stations produce different total_times ─────────────────────


class TestStationVariation:
    """Tests that stations with different seeds produce different results."""

    def test_all_stations_have_different_total_times(self) -> None:
        """All 4 stations produce distinct total_time values."""
        total_times = [run_station(i)["total_time"] for i in range(4)]
        assert len(set(total_times)) == 4, (
            f"Expected 4 unique total_times, got {total_times}"
        )


# ── accuracy_score is in (0, 1] ──────────────────────────────────────


class TestAccuracyScore:
    """Tests for injection accuracy score bounds."""

    @pytest.mark.parametrize("idx", range(4))
    def test_accuracy_in_valid_range(self, idx: int) -> None:
        """injection_accuracy is in the half-open interval (0, 1]."""
        metrics = run_station(idx)
        accuracy = metrics["injection_accuracy"]
        assert 0.0 < accuracy <= 1.0, f"Station {idx} accuracy {accuracy} not in (0, 1]"


# ── ppo_reward is finite ─────────────────────────────────────────────


class TestPpoReward:
    """Tests for PPO reward values."""

    @pytest.mark.parametrize("idx", range(4))
    def test_reward_is_finite(self, idx: int) -> None:
        """ppo_reward is a finite number (not NaN or inf)."""
        metrics = run_station(idx)
        assert math.isfinite(metrics["ppo_reward"]), (
            f"Station {idx} reward {metrics['ppo_reward']} is not finite"
        )

    @pytest.mark.parametrize("idx", range(4))
    def test_reward_is_float(self, idx: int) -> None:
        """ppo_reward is a numeric type."""
        metrics = run_station(idx)
        assert isinstance(metrics["ppo_reward"], (int, float))


# ── Rankings are assigned correctly after run_competition ────────────


class TestRankings:
    """Tests for competition ranking logic."""

    def test_rankings_are_assigned(self) -> None:
        """After run_competition all stations have non-zero ranks."""
        result = run_competition()
        for station in result["stations"]:
            assert station["rank"] > 0, (
                f"Station {station['station_id']} has rank 0 (unassigned)"
            )

    def test_rankings_are_unique(self) -> None:
        """Each station receives a unique rank from 1 to 4."""
        result = run_competition()
        ranks = sorted(s["rank"] for s in result["stations"])
        assert ranks == [1, 2, 3, 4]

    def test_rank_1_has_lowest_total_time(self) -> None:
        """The station ranked #1 has the smallest total_time."""
        result = run_competition()
        stations = result["stations"]
        rank1 = next(s for s in stations if s["rank"] == 1)
        for station in stations:
            assert rank1["total_time"] <= station["total_time"]

    def test_winner_matches_rank_1(self) -> None:
        """The winner field matches the station_id of rank 1."""
        result = run_competition()
        rank1 = next(s for s in result["stations"] if s["rank"] == 1)
        assert result["winner"] == rank1["station_id"]

    def test_competition_has_four_stations(self) -> None:
        """Competition result contains exactly 4 stations."""
        result = run_competition()
        assert len(result["stations"]) == 4
