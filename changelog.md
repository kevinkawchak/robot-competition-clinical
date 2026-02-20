# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [v0.1.0] - 2026-02-20

### Added
- MuJoCo MJCF clinical scene model with G1 humanoid robots (doctor, nurse, patient)
- Three.js cross-device web viewer with 3D interactive simulation
- Deltoid intramuscular injection procedure animation (cancer medication delivery)
- Play/pause controls, progress bar scrubbing, and speed display
- File upload button for custom scene data (JSON/XML)
- Python simulation runner (`simulation/run_simulation.py`) with MuJoCo physics
- Animation export utility (`simulation/export_animation.py`) for web viewer data
- Responsive UI supporting desktop, iOS, and Android browsers
- Medical equipment models: IV stand, instrument tray, vitals monitor, examination chair
- Role-based robot differentiation: doctor (white shell + red cross), nurse (blue shell + badge), patient (green gown)
- Injection site targeting on patient deltoid (upper arm) with visual marker
- CI workflow with ruff lint and format checks for Python 3.10, 3.11, 3.12
- GitHub Pages deployment support via `docs/` folder
- Comprehensive README with 3 text-based architecture diagrams
- Project configuration via `pyproject.toml`
- Attribution to mjlab (mujocolab/mjlab) throughout

### Technical Details
- Physics engine: MuJoCo (via MJCF XML scene definition)
- Web rendering: Three.js r169 with OrbitControls
- CI/CD: GitHub Actions with ruff linter
- Zero-install viewing via GitHub Pages (static HTML/JS)

[v0.1.0]: https://github.com/kevinkawchak/robot-competition-clinical/releases/tag/v0.1.0
