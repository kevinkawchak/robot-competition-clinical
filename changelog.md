# Changelog

All notable changes to this project will be documented in this file.

## [0.7.0] — 2026-03-04

### Added
- **v0.7.0 competition viewer** (`docs/v7/index.html`) with enhanced hospital visuals
- **Hospital environment details** — ceiling with light fixtures per station quadrant, baseboards
  along all walls, wooden door with frame and handle on back wall
- **Patient facial features** — eyes with pupils, eyebrows, nose, and mouth on human patient model
- **G1 torso segmentation** — chest and abdomen split with metallic seam joint, separate front panels
- **Active nurse animation** — nurse G1 animates throughout all 7 phases (not just monitoring),
  with tablet checking, head tracking toward patient, and left arm movement
- **Patient reactive animation** — patient turns head toward doctor during injection, left hand
  grip tightens during inject phase
- **Nurse G1 LED mask pulse** — nurse visor LED pulses at offset frequency from doctor
- **Four-version nav banner** — clickable links to v0.1.0, v0.5.0, v0.6.0, and v0.7.0 (current)

### Changed
- Nav banner now shows four versions: v0.1.0 | v0.5.0 | v0.6.0 | v0.7.0 (current)
- Updated v0.1.0, v0.5.0, v0.6.0 viewer nav banners to include v0.7.0 link
- Updated `pyproject.toml` version from 0.6.0 to 0.7.0
- Updated `simulation_v2/run_competition.py` version string to 0.7.0
- Updated `simulation_v2/export_competition.py` version string to 0.7.0
- Updated `tests/test_exports.py` to expect version 0.7.0
- Updated README with v0.7.0 documentation and version table
- Increased tone mapping exposure from 1.4 to 1.5 for enhanced lighting

## [0.6.0] — 2026-03-03

### Added
- **v0.6.0 competition viewer** (`docs/v6/index.html`) with realistic Unitree G1 humanoid robots
  (from unitreerobotics) as doctors and nurses, and a realistic human patient
- **Realistic Unitree G1 robot models** — dark charcoal body panels, glossy black visor head,
  metallic silver joints, three-fingered dexterous hands (Dex3-1), 23–43 DOF articulation,
  matching the real G1's 1.32m height and compact industrial design
- **Human patient model** — skin-colored human figure with proper anatomy (head with hair,
  arms, legs), wearing green hospital gown, seated correctly facing forward in exam chair
- **Doctor G1 robot** wears semi-transparent white medical coat overlay with red cross emblem,
  firmly holds syringe in right dexterous hand with visible grip
- **Nurse G1 robot** wears semi-transparent blue medical coat overlay with gold badge,
  holds tablet/clipboard for monitoring
- **Injection target on patient** — red pulsing marker placed directly on patient's right
  deltoid (upper arm), not floating in space
- **Smoother robot animations** — finer interpolation for more natural doctor arm movements
  during 7-phase injection procedure
- **Lowered station labels** — "Station A/B/C/D" labels positioned closer to robot heads
  (y=2.4) instead of floating too high above (was y=3.2)
- **Three-version nav banner** — clickable links to v0.1.0, v0.5.0, and v0.6.0 (current)
- **v0.6.0 release notes** in `releases.md`
- **v0.6.0 build prompt** in `prompts.md`
- **v0.5.0 architecture diagrams** archived in `docs/diagrams/v5_architecture.md`

### Changed
- **Nav banner** now shows three versions: v0.1.0 | v0.5.0 | v0.6.0 (current)
- Updated v0.1.0 viewer nav banner to link to v0.5.0 and v0.6.0
- Updated v0.5.0 viewer nav banner to link to v0.1.0 and v0.6.0
- Updated `pyproject.toml` version from 0.5.0 to 0.6.0
- Updated `simulation_v2/run_competition.py` version string to 0.6.0
- Updated `simulation_v2/export_competition.py` version string to 0.6.0
- Updated `tests/test_exports.py` to expect version 0.6.0
- Updated README with v0.6.0 documentation, version table with release links, new diagrams
- Robot models upgraded from basic CapsuleGeometry humanoids to realistic Unitree G1 representation
- Patient model changed from robot to realistic human figure

### Fixed
- **Patient orientation**: Patient now sits facing forward in the chair (was reversed in v0.5.0)
- **Patient anatomy**: Patient now has arms that rest on armrests (was missing arms)
- **Patient legs**: Legs hang correctly in front of chair (were extending through backrest)
- **Injection target placement**: Red target marker now positioned on patient's actual right
  deltoid arm surface (was floating detached from patient)
- **Doctor holding needle**: Syringe firmly attached to doctor's dexterous hand with visible
  grip (was loosely positioned)
- **Station label height**: Labels lowered from y=3.2 to y=2.4, closer to station participants
- **Robot movement quality**: Smoother, less coarse animations with additional interpolation steps

## [0.5.0] — 2026-02-22

### Added
- **v0.5.0 competition viewer** (`docs/v5/index.html`) replicating v0.1.0's exact station
  layout across 4 competing stations in a 2x2 grid
- **Open-top building** — ceiling removed so viewers can see through the hospital room
- **v0.1.0 articulated humanoids** with full joint hierarchy: shoulder, elbow, wrist pivots
  enabling realistic doctor injection animation with CapsuleGeometry limbs, joint rings
  at every articulation point, and role markers (red cross, gold badge)
- **v0.1.0 7-phase procedure** per station: prepare, approach, position, inject, hold,
  withdraw, monitor — doctor performs injection with syringe (matching v0.1.0 exactly)
- **Doctor holds syringe** (right of patient) — v0.1.0 layout restored
- **Nurse holds tablet** (left of patient) — v0.1.0 layout restored
- **Full medical equipment per station**: IV stand with hook/tube/3-arm base, instrument
  tray with spare syringe/vials/swab/rim, vitals monitor with base/screen/LED, exam chair
  with armrest supports and cushions
- **Archived v0.4.0 diagrams** in `docs/diagrams/v4_architecture.md`
- **v0.5.0 release notes** in `releases.md`
- **v0.5.0 build prompt** in `prompts.md`

### Changed
- **Nav banner** now links only v0.1.0 and v0.5.0 (removed v0.3.0/v0.4.0 links)
- Updated v0.1.0 viewer nav banner to link to v0.5.0 (was linking to v0.4.0)
- Updated `pyproject.toml` version from 0.4.0 to 0.5.0
- Updated `simulation_v2/run_competition.py` version string to 0.5.0
- Updated `simulation_v2/export_competition.py` version string to 0.5.0
- Updated `tests/test_exports.py` to expect version 0.5.0
- Updated README with v0.5.0 documentation, new architecture diagrams, simulation details
- All stations use v0.1.0's 7-phase doctor injection procedure instead of v0.4.0's
  4-phase doctor review + 6-phase nurse injection split
- Station layout matches v0.1.0: doctor (right, syringe), nurse (left, tablet)

### Fixed
- **Building visibility**: removed ceiling so camera can see through the room from above
- **Station fidelity**: stations now exactly replicate v0.1.0's robot detail, props, and
  joint articulation rather than the simplified v0.4.0 layout

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
