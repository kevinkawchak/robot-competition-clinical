"""Tests for exported payload boundaries and schema correctness.

Peer review fix #6: Validate exported animation and competition
payloads include required fields, correct terminal frames, and
consistent versioning.
"""

from simulation.export_animation import generate_web_animation
from simulation_v2.export_competition import generate_competition_animation


class TestV1ExportPayload:
    """Validate the v0.1.x single-station export payload."""

    def test_has_required_fields(self) -> None:
        data = generate_web_animation(fps=10)
        required = {
            "version",
            "simulation",
            "description",
            "attribution",
            "duration",
            "fps",
            "total_frames",
            "phases",
            "keyframes",
        }
        assert required.issubset(data.keys())

    def test_version_format(self) -> None:
        data = generate_web_animation(fps=10)
        parts = data["version"].split(".")
        assert len(parts) == 3
        assert all(p.isdigit() for p in parts)

    def test_keyframes_non_empty(self) -> None:
        data = generate_web_animation(fps=10)
        assert len(data["keyframes"]) > 0

    def test_terminal_frame_at_duration(self) -> None:
        data = generate_web_animation(fps=10)
        last = data["keyframes"][-1]
        assert last["t"] >= data["duration"] - 0.01

    def test_phases_non_empty(self) -> None:
        data = generate_web_animation(fps=10)
        assert len(data["phases"]) > 0

    def test_keyframe_has_doctor_and_nurse(self) -> None:
        data = generate_web_animation(fps=10)
        kf = data["keyframes"][0]
        assert "doctor" in kf
        assert "nurse" in kf


class TestV2ExportPayload:
    """Validate the v0.2+ competition export payload."""

    def test_has_required_fields(self) -> None:
        data = generate_competition_animation(fps=10)
        required = {
            "version",
            "simulation",
            "description",
            "attribution",
            "num_stations",
            "fps",
            "ppo_config",
            "stations",
            "winner",
        }
        assert required.issubset(data.keys())

    def test_version_is_project_aligned(self) -> None:
        data = generate_competition_animation(fps=10)
        assert data["version"] == "0.4.0"

    def test_four_stations_exported(self) -> None:
        data = generate_competition_animation(fps=10)
        assert len(data["stations"]) == 4

    def test_each_station_has_keyframes(self) -> None:
        data = generate_competition_animation(fps=10)
        for st in data["stations"]:
            assert "keyframes" in st
            assert len(st["keyframes"]) > 0

    def test_station_terminal_frame(self) -> None:
        data = generate_competition_animation(fps=10)
        for st in data["stations"]:
            last_kf = st["keyframes"][-1]
            assert last_kf["t"] >= st["total_time"] - 0.2

    def test_winner_is_valid_station_id(self) -> None:
        data = generate_competition_animation(fps=10)
        ids = {s["station_id"] for s in data["stations"]}
        assert data["winner"] in ids

    def test_ppo_config_has_required_keys(self) -> None:
        data = generate_competition_animation(fps=10)
        ppo = data["ppo_config"]
        assert "architecture" in ppo
        assert "reward_weights" in ppo
        assert "gamma" in ppo

    def test_ranks_assigned(self) -> None:
        data = generate_competition_animation(fps=10)
        ranks = {s.get("rank") for s in data["stations"]}
        assert ranks == {1, 2, 3, 4}
