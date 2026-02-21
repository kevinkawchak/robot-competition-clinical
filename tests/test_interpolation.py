"""Unit tests for interpolation and validation helpers."""

from __future__ import annotations

import sys
from unittest.mock import MagicMock

import pytest

from simulation.constants import validate_fps
from simulation.export_animation import smooth_step
from simulation_v2.ppo_policy import smooth_interp as ppo_smooth_interp

# simulation.run_simulation imports mujoco at the top level.  When that
# optional dependency is not installed we insert a MagicMock stub so
# the module can still be imported and we can test smooth_interp.
if "mujoco" not in sys.modules:
    sys.modules["mujoco"] = MagicMock()

from simulation.run_simulation import smooth_interp as sim_smooth_interp  # noqa: E402

# ── smooth_interp from simulation.run_simulation ────────────────────


class TestSimSmoothInterp:
    """Tests for simulation.run_simulation.smooth_interp."""

    def test_boundary_zero(self) -> None:
        """f(0) returns 0."""
        assert sim_smooth_interp(0.0) == pytest.approx(0.0)

    def test_boundary_one(self) -> None:
        """f(1) returns 1."""
        assert sim_smooth_interp(1.0) == pytest.approx(1.0)

    def test_monotonicity(self) -> None:
        """f(0.25) < f(0.5) < f(0.75)."""
        v25 = sim_smooth_interp(0.25)
        v50 = sim_smooth_interp(0.50)
        v75 = sim_smooth_interp(0.75)
        assert v25 < v50 < v75

    def test_clamping_below(self) -> None:
        """f(-1) is clamped to 0."""
        assert sim_smooth_interp(-1.0) == pytest.approx(0.0)

    def test_clamping_above(self) -> None:
        """f(2) is clamped to 1."""
        assert sim_smooth_interp(2.0) == pytest.approx(1.0)

    def test_midpoint_value(self) -> None:
        """f(0.5) equals 0.5 (smoothstep symmetry)."""
        assert sim_smooth_interp(0.5) == pytest.approx(0.5)


# ── smooth_step from simulation.export_animation ────────────────────


class TestExportSmoothStep:
    """Tests for simulation.export_animation.smooth_step."""

    def test_boundary_zero(self) -> None:
        """f(0) returns 0."""
        assert smooth_step(0.0) == pytest.approx(0.0)

    def test_boundary_one(self) -> None:
        """f(1) returns 1."""
        assert smooth_step(1.0) == pytest.approx(1.0)

    def test_monotonicity(self) -> None:
        """f(0.25) < f(0.5) < f(0.75)."""
        v25 = smooth_step(0.25)
        v50 = smooth_step(0.50)
        v75 = smooth_step(0.75)
        assert v25 < v50 < v75

    def test_clamping_below(self) -> None:
        """f(-1) is clamped to 0."""
        assert smooth_step(-1.0) == pytest.approx(0.0)

    def test_clamping_above(self) -> None:
        """f(2) is clamped to 1."""
        assert smooth_step(2.0) == pytest.approx(1.0)

    def test_midpoint_value(self) -> None:
        """f(0.5) equals 0.5 (smoothstep symmetry)."""
        assert smooth_step(0.5) == pytest.approx(0.5)


# ── smooth_interp from simulation_v2.ppo_policy ────────────────────


class TestPpoSmoothInterp:
    """Tests for simulation_v2.ppo_policy.smooth_interp."""

    def test_boundary_zero(self) -> None:
        """f(0) returns 0."""
        assert ppo_smooth_interp(0.0) == pytest.approx(0.0)

    def test_boundary_one(self) -> None:
        """f(1) returns 1."""
        assert ppo_smooth_interp(1.0) == pytest.approx(1.0)

    def test_monotonicity(self) -> None:
        """f(0.25) < f(0.5) < f(0.75)."""
        v25 = ppo_smooth_interp(0.25)
        v50 = ppo_smooth_interp(0.50)
        v75 = ppo_smooth_interp(0.75)
        assert v25 < v50 < v75

    def test_clamping_below(self) -> None:
        """f(-1) is clamped to 0."""
        assert ppo_smooth_interp(-1.0) == pytest.approx(0.0)

    def test_clamping_above(self) -> None:
        """f(2) is clamped to 1."""
        assert ppo_smooth_interp(2.0) == pytest.approx(1.0)

    def test_midpoint_value(self) -> None:
        """f(0.5) equals 0.5 (smoothstep symmetry)."""
        assert ppo_smooth_interp(0.5) == pytest.approx(0.5)


# ── validate_fps ────────────────────────────────────────────────────


class TestValidateFps:
    """Tests for simulation.constants.validate_fps."""

    def test_raises_for_zero(self) -> None:
        """fps=0 raises ValueError."""
        with pytest.raises(ValueError, match="fps must be >= 1"):
            validate_fps(0)

    def test_raises_for_negative(self) -> None:
        """fps=-5 raises ValueError."""
        with pytest.raises(ValueError, match="fps must be >= 1"):
            validate_fps(-5)

    def test_accepts_one(self) -> None:
        """fps=1 (the minimum) does not raise."""
        validate_fps(1)  # Should not raise

    def test_accepts_thirty(self) -> None:
        """fps=30 does not raise."""
        validate_fps(30)  # Should not raise

    def test_accepts_large_value(self) -> None:
        """fps=240 does not raise."""
        validate_fps(240)  # Should not raise
