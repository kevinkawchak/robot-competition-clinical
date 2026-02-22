# Changelog

All notable changes to this project will be documented in this file.

## [0.4.0] — 2026-02-22

### Added
- **Light-mode competition viewer** (`docs/v4/index.html`) with white/light theme (#e8ecf0)
  for easier zooming into individual stations
- **Full-detail G1 humanoid robots** matching v0.1.0 articulation: joint rings at
  shoulders/elbows/hips/knees, visors, pelvis, separate thigh/shin segments, hands
- **Role markers**: red cross emblem on doctor chest, gold badge on nurse chest
- **Pulsing injection target**: animated ring with center dot on patient right deltoid
- **Full medical equipment**: IV stand with hook/tube/3-arm base, instrument tray with
  spare syringe/vials/swab, monitor with base stand/screen/LED indicator, exam chair
  with armrest supports
- **Metrics reset**: full state reset between competition runs (elapsed, phase, finish
  order all properly zeroed)
- **Results-only overlay**: "Close Results" button instead of auto-replay; user manually
  replays via Reset button
- **16m x 16m hospital room** with 5.5m grid spacing (up from 14m/5.0m)
- **Cross-viewer nav banner** linking v0.1.0 (stable) and v0.4.0 (current)
- **Archived v0.3.0 diagrams** in `docs/diagrams/v3_architecture.md`
- **Release notes** in `releases.md`
- **Build prompt** stored in `prompts.md`

### Changed
- Updated v0.1.0 viewer nav banner to link to v0.4.0 (was linking to v0.3.0 at `/v2/`)
- Updated `pyproject.toml` version from 0.3.0 to 0.4.0
- Updated `simulation_v2/run_competition.py` version string to 0.4.0
- Updated `simulation_v2/export_competition.py` version string to 0.4.0
- Updated `tests/test_exports.py` to expect version 0.4.0
- Updated README with v0.4.0 documentation, new architecture diagrams, comparison tables
- All stations face +Z direction (consistent with v0.1.0 orientation)
- Station participants oriented consistently: doctor (left), patient (center), nurse (right)

### Fixed
- **GitHub Pages version mismatch**: v0.3.0 content was served at `/v2/` path; v0.4.0
  now correctly served at `/v4/` path
- **Metrics not resetting**: scoreboard and phase indicators now fully reset between runs
- **Results overlay**: replaced "Close & Replay" auto-behavior with clean "Close Results"
  button that does not auto-reset; user controls replay via Reset button

## [0.3.0] — 2025-12-15

### Added
- Closable scoreboard and phase timeline panels with toggle buttons
- Final results overlay showing 1st/2nd/3rd/4th rankings
- Cross-viewer navigation banner (v0.1.x <-> v0.3.0)
- Station selector with camera transitions (Overview/A/B/C/D)
- JSON upload with schema validation for custom configs
- `docs/diagrams/v2_viewer_modules.md` — internal module map
- Export boundary tests in `tests/test_exports.py`

### Changed
- Viewer at `docs/v2/index.html` now includes dark theme
- 14m x 14m hospital room with 5.0m grid spacing
- Updated README diagrams for v0.3.0

## [0.2.0] — 2025-12-01

### Added
- **4-station competition simulation** with PPO-trained policies
- `simulation_v2/` package: `constants.py`, `ppo_policy.py`, `run_competition.py`,
  `export_competition.py`
- 4 per-station PPO configurations with unique random seeds (42, 137, 256, 512)
- PPO reward function: R = -0.3*time + 0.5/(1+dist) + 0.2/(1+jerk)
- Competition ranking by total time with accuracy tiebreaker
- `docs/v2/index.html` — Three.js competition viewer for GitHub Pages
- 2x2 grid layout with 12 G1 humanoid robot models
- `tests/test_competition.py` — unit tests for competition metrics
- Archived v0.1.x diagrams to `docs/diagrams/v1_architecture.md`

### Changed
- Updated project description and README for multi-station competition

## [0.1.1] — 2025-11-15

### Changed
- Peer review implementation: 14 senior review recommendations
- Added TypedDict structures for type safety
- Added MuJoCo dependency guard (graceful fallback)
- Added terminal frame boundary in exports
- Improved smoothstep interpolation clamping
- Added comprehensive test suite (phases, interpolation, exports)

## [0.1.0] — 2025-11-01

### Added
- Initial release: single-station clinical injection simulation
- G1 humanoid robots: doctor, nurse, patient
- 7-phase injection procedure (prepare through monitor)
- MuJoCo MJCF scene model with physics
- Three.js web viewer (`docs/index.html`) for GitHub Pages
- Play/pause, progress scrub, file upload, info panel
- Mobile-responsive design (iOS, Android, desktop)
