# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [v0.3.0] - 2026-02-22

### Added
- Completely rebuilt v2 competition viewer (`docs/v2/index.html`) with closable scoreboard and phase timeline panels
- Final results overlay showing clear 1st/2nd/3rd/4th ranking with times and accuracies
- Cross-navigation banner in both HTML viewers (root ↔ v2) with base-path-aware links
- Injection target marker (red dot) on each patient's deltoid muscle
- Export boundary tests (`tests/test_exports.py`) — 14 new tests for payload schema validation
- `PpoConfig` TypedDict for type-safe PPO configuration in `simulation_v2/constants.py`
- Archived v0.2.0 diagrams to `docs/diagrams/v2_architecture.md`
- Peer review implementation report at `peer-review/v0.3.0-implementation-report.md`
- v0.3.0 build prompt stored in `prompts.md`
- Smoke command docs in README (pytest, ruff)

### Changed
- `docs/v2/index.html` — full rewrite: removed divider boxes hiding stations, added toggle-based panels, mobile-optimized responsive breakpoints, JSON upload validation, station finish-order tracking
- `docs/index.html` — added navigation banner with link to v2 competition viewer
- `README.md` — full clickable URLs for both simulations, updated project structure with new files, detailed PPO documentation (same policy, different state), measurement methodology, closable UI features
- `simulation_v2/constants.py` — added `PpoConfig` TypedDict (peer review fix #4)
- `simulation_v2/run_competition.py` — version string `"2.0.0"` → `"0.3.0"` (peer review fix #2)
- `simulation_v2/export_competition.py` — version string `"2.0.0"` → `"0.3.0"` (peer review fix #2)
- `simulation/export_animation.py` — added explicit terminal frame at `TOTAL_DURATION` (peer review fix #3)
- `pyproject.toml` — version bumped to 0.3.0
- `prompts.md` — added v0.3.0 build prompt
- `changelog.md` — added v0.3.0 release entry
- `releases.md` — added v0.3.0 release notes

### Fixed
- Phase timeline and scoreboard overlapping visual elements (now closable)
- Stations appearing hidden inside large box dividers (removed dividers, proper grid)
- Payload version inconsistency: `"2.0.0"` → `"0.3.0"` to align with project semver (peer review fix #2)
- Missing terminal frame in v1 export animation (peer review fix #3)
- Loose `ppo_config` typing: `dict[str, float]` → `PpoConfig` TypedDict (peer review fix #4)
- GitHub Pages path portability: base-path-aware cross-viewer navigation (peer review fix #1)
- Missing JSON upload validation in v2 viewer (peer review fix #5)
- No competition completion display — now shows final results overlay
- Mobile layout issues on iPhone/Android — three responsive breakpoints (768px, 420px)

## [v0.2.1] - 2026-02-21

### Added
- Senior engineering peer-review report for v0.2.1 with implementation-ready recommendations for Claude (`peer-review/v0.2.1-senior-peer-review.md`)
- GitHub Pages directory portability resolution plan documenting how to make both root and `/v2/` simulations reliably accessible from different paths/forks
- Peer-review metrics for coverage, severity counts, and estimated implementation effort

### Changed
- Updated release documentation for v0.2.1 to capture review outcomes, contributors, and next-step implementation focus

### Notes
- This release entry records peer-review guidance and release notes updates only; no simulation runtime code was modified in v0.2.1.

## [v0.2.0] - 2026-02-21

### Added
- 4-station clinical competition simulation with 2x2 grid layout in a larger hospital room
- PPO reinforcement learning policies — each station uses the same MLP architecture (64x64, tanh) trained with different random seeds, producing distinct behavior profiles
- Doctor-on-left / Nurse-on-right layout — doctor (white coat) reviews symptoms/toxicities; nurse (blue coat) performs the injection to the patient's nearest arm
- Competition scoreboard showing doctor review time, nurse injection time, total time, injection accuracy, and rank for all 4 stations simultaneously
- Per-station timing and accuracy measurement accessible through mobile-friendly control buttons
- Shared constants module (`simulation/constants.py`) centralizing phase timings and type-safe data structures (TypedDict)
- `simulation_v2` package — multi-station competition runner, PPO policy simulation, and animation exporter
- Separate GitHub Pages viewer at `/docs/v2/index.html` for the competition simulation
- MuJoCo MJCF competition scene (`simulation_v2/models/competition_scene.xml`) with 4 complete stations
- Unit test suite (`tests/`) covering phase transitions, interpolation, FPS validation, and competition metrics
- Pre-commit configuration (`.pre-commit-config.yaml`) with ruff hooks
- Original v0.1.x architecture diagrams archived to `docs/diagrams/v1_architecture.md`
- 3 new comprehensive text diagrams in README for v0.2.0
- v0.2.0 build prompt stored in `prompts.md`

### Changed
- `simulation/run_simulation.py` — applied all critical/high peer-review fixes
- `simulation/export_animation.py` — added FPS validation, explicit UTF-8 encoding, shared constants
- `README.md` — rewritten with v0.2.0 competition scenario, new diagrams, dual GitHub Pages links
- `pyproject.toml` — version bumped to 0.2.0, added pytest dependency
- `.github/workflows/ci.yml` — expanded CI with smoke tests

### Fixed
- FPS <= 0 causing division-by-zero (peer review #1)
- `mj_name2id` returning -1 silently reading wrong site (peer review #2)
- Truncated final frame in simulation capture (peer review #3)
- Broad `except Exception` hiding runtime defects (peer review #4)
- Repeated `mj_name2id` calls inside simulation loop (peer review #5)
- Implicit file encoding in JSON I/O (peer review #7)
- Duplicated phase constants across modules (peer review #8)

## [v0.1.1] - 2026-02-21

### Added
- Senior engineering peer-review report for v0.1.1 with prioritized fix recommendations and implementation order (`peer-review/v0.1.1-senior-peer-review.md`)

### Changed
- Updated release documentation for v0.1.1 with summary, feature-level review outcomes, contributors, and notes

### Notes
- This release entry records review outcomes and recommendations only; no production code behavior changes are included in v0.1.1.

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

[v0.3.0]: https://github.com/kevinkawchak/robot-competition-clinical/releases/tag/v0.3.0
[v0.2.0]: https://github.com/kevinkawchak/robot-competition-clinical/releases/tag/v0.2.0
[v0.2.1]: https://github.com/kevinkawchak/robot-competition-clinical/releases/tag/v0.2.1
[v0.1.1]: https://github.com/kevinkawchak/robot-competition-clinical/releases/tag/v0.1.1
[v0.1.0]: https://github.com/kevinkawchak/robot-competition-clinical/releases/tag/v0.1.0
