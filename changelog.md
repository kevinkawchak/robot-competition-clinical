# Changelog

All notable changes to this project will be documented in this file.

## [1.1.0] — 2026-06-11

### Added
- **v1.1.0 Real-Life GCP Suite viewer** (`docs/v11/index.html`) — everything made real
  life on top of the v1.0.0 GCP Trial Suite, still open-top (no ceiling)
- **Real Unitree H2 robot files**: doctor and nurse are the actual **Unitree H2 Plus**
  (H2 + dual SHARPA dexterous hands) — visual meshes and the full physics joint tree
  (75 revolute joints with axes and limits) converted from
  `kevinkawchak/fork_unitree_model` `H2_Plus/H2_with_sharpa.usdz` (binary USD crate) into
  `docs/v11/h2_plus.glb` (3.7 MB, 151k triangles, joint metadata in node extras), loaded
  same-origin with GLTFLoader and articulated live; simplified procedural fallback
  humanoids if the GLB cannot be fetched (e.g. `file://`)
- **`tools/convert_h2_usd_to_glb.py`** — offline converter (usd-core +
  fast-simplification): welds the unindexed USD triangle soup, decimates 744k → 151k
  triangles (fingers harder than shells), recomputes normals, preserves the joint tree
  with per-node `{joint, axis, lo, hi}` extras, and verifies forward kinematics against
  the authored USD link poses (max error 0.0001 mm)
- **Realistic patients v2**: layered torsos, five-finger articulated hands, expressive
  faces (eyelids, brows, lips, ears, cheeks, jaw), ECG chest leads with sagging cable,
  per-station personas — calm / talkative (chats with the nurse, lips move) / anxious
  (faster blink, finger fidget, watches the needle, early armrest grip) / elderly
  (reading glasses, grey bun, slower head, light hand tremor)
- **Naturally dissimilar stations**: each seed draws a motion style (stride, cadence,
  waist lean, arm reach, head energy, walk-path bow, pose tempo, walk bounce) and a
  staggered visit start (0.66–1.75 s); metric draws are profile-correlated (speed station
  faster + sloppier needle, precision station tighter + steadier), so movements and
  scores differ naturally — deterministic results: D 96.6 (0.33 mm), A 89.0, C 85.6
  (AE Gr.1), B 82.2 (fastest wall finish, ranks last)
- **Infinite zoom from any point**: custom fly-through dolly replaces OrbitControls
  zoom — no minimum or maximum distance, wheel and pinch both supported, zoom-to-cursor,
  the orbit pivot glides through geometry so travel never stalls, adaptive near/far clip
  planes (razor-sharp at millimeter range, no clipping at building range)
- **Real-life open-air suite**: physically-modeled daylight sky (three.js Sky) over the
  open-top room, 20 m × 20 m floorplan, wall bumper rails, live wall clock (real local
  time), scrub sink with towel dispenser, red crash cart with defib, supply shelving,
  per-station medical-gas outlet panels, EXIT sign over the door, potted plants, outdoor
  apron so fly-out zoom never shows a void
- **Signage v2 (fixes low-res clipped headings)**: every poster/label/board re-rendered
  at 4x resolution (2048-px posters) with measure-and-fit headline sizing and word-wrapped
  body text; posters get aluminium frames; max-anisotropy sampling

### Changed
- Nav banners in v0.1.0, v0.5.0–v0.9.0, and v1.0.0 viewers updated to link v1.1.0 at the
  far right ("v1.0.0 (new)" labels demoted to "v1.0.0"); `docs/404.html` lists v11/
- `pyproject.toml` version from 1.0.0 to 1.1.0
- README rewritten around v1.1.0: version table, real-robot-file pipeline, persona/motion
  style documentation, deterministic results, architecture diagrams, project structure,
  Unitree H2 attribution
- ECG monitor screens at 512×288 (sharper traces), scoreboard tower at 1024×768
- Hand-IK tip correction is incremental (accumulates from the current offset) so the
  needle/swab tip converges exactly onto the deltoid instead of halving the error

### Fixed
- **Low-resolution signage with clipped headings** (e.g. "ONCOLOGY CLINICAL TRIALS UNIT"
  overflowing the poster band in v1.0.0): headings now measure-and-fit, bodies word-wrap
- **Zoom stops** (v1.0.0 clamped 0.05–48 m): zoom is now infinite in both directions from
  any point, through geometry
- **Identical station choreography**: stations no longer share one keyframe timing — style
  parameters, staggered starts and per-phase tempo make every station visibly different

## [1.0.0] — 2026-06-10

### Added
- **v1.0.0 GCP Trial Suite viewer** (`docs/v10/index.html`) — ground-up state-of-the-art
  rebuild of the nurse/doctor/patient competition for clinical trial experts
- **12-phase GCP visit workflow** per station: identity verification, eConsent, baseline
  vitals, hand hygiene, drug prep + barcode check, aseptic site prep, landmark/alignment,
  needle insertion, 0.50 mL dose delivery, withdraw + safety, sharps disposal, observation
  + eSource documentation — each phase tagged with its acting role (N/D)
- **High-DOF Unitree G1 robots** (43 DOF incl. Dex3-1 hands): articulated 2-segment fingers
  that grip tools, 3-DOF waist, 2-DOF neck, wrist supination, 6-DOF legs with a gait cycle
  whenever the robot root translates
- **IK-lite tip correction** — needle tip is servo-driven onto the deltoid target every
  frame (surface at insertion, 6 mm indwelling during dose); horizontal error feeds a
  natural whole-robot "step-in" so corrections never detach the wrist
- **Composite GCP scoring** — 0.30×Time + 0.25×Accuracy + 0.20×Protocol + 0.10×Sterility +
  0.10×Dose + 0.05×Comfort; ranking by composite (raw-time ranking retired)
- **Seeded Grade 1 vasovagal adverse event** at exactly one station (C): ECG dips to
  ~49 bpm, patient head droops, nurse responds, observation extends, scoreboard AE flag
- **Live animated ECG/SpO2/NIBP monitors** per station (canvas-texture P-QRS-T waveform)
- **Central 4-face live scoreboard tower** with ranks, composite scores, progress, AE flags
- **Human CRA at a sponsor monitoring desk** with live EDC laptop screen — human-in-the-loop
  trial oversight (types, scans the room, blinks, breathes)
- **Diverse realistic patients** — per-station skin tone, hairstyle, gown color; blinking,
  breathing, consent nods, injection head-turn, armrest grip
- **Photoreal open-top room** (no ceiling): procedural vinyl-tile floor and wainscot wall
  textures, observation window + hallway, wooden door, clinical signage posters, privacy
  screens, freestanding exam-light booms, infusion pumps, supply carts with drawers/vials/
  gloves/swabs, sharps containers, sanitizer stands, waste bins, station floor decals
- **Zoom-anywhere camera**: minDistance 0.05 m, zoom-to-cursor, fog removed, double-click /
  double-tap glide-focus on any object, keyboard shortcuts (Space, R, 0–4)
- **Live telemetry panel**: DOF count, phase, live needle→target mm, recorded deviation,
  dose delivered, heart rate, eSource latency, AE status
- **Seven-version nav banner** with v1.0.0 farthest right (v0.1.0 … v0.9.0 | v1.0.0)
- v1.0.0 release notes in `releases.md`, build prompt in `prompts.md`

### Changed
- Nav banners in v0.1.0, v0.5.0, v0.6.0, v0.7.0, v0.8.0, and v0.9.0 viewers updated to
  link v1.0.0 at the far right ("v0.9.0 (new)" labels demoted to "v0.9.0")
- `pyproject.toml` version from 0.9.0 to 1.0.0
- `simulation_v2/run_competition.py` version string from 0.9.0 to 1.0.0
- `simulation_v2/export_competition.py` version string from 0.9.0 to 1.0.0
- `tests/test_exports.py` to expect version 1.0.0
- README rewritten around v1.0.0: version table, GCP workflow, composite scoring,
  architecture diagrams, project structure
- Station speed profiles retuned for the 18.5 s-base 12-phase visit
  (A 1.00 / B 0.93 / C 1.07 / D 0.97)
- Ranking now by composite GCP score with total-time tiebreak

### Fixed
- **Physical object overlap (all stations)**: coats are part of the torso shell (z-fighting
  impossible), all props placed with verified clearances and seated flush on surfaces
  (tray syringe and sharps container no longer float), patient pelvis rests on the cushion
  with thighs at 3 mm compression and soles exactly on the floor (shin segments corrected),
  robot soles exactly on the floor
- **Needle contact**: IK tip correction guarantees frame-accurate needle-to-deltoid contact
  at every station regardless of pose interpolation — no interpenetration, no air gap
- **Monitor orientation**: vitals screens face the nurse (previous releases faced away)
- **Equipment lighting**: per-station exam lights are freestanding booms (consistent with
  the no-ceiling room) instead of ceiling fixtures

## [0.9.0] — 2026-05-01

### Added
- **v0.9.0 competition viewer** (`docs/v9/index.html`) — targeted-fix release built on the
  strong-performing v0.6.0 base
- **Patient facial features** — eyes (whites + pupils), eyebrows, nose, mouth, chin,
  hair cap with fringe so the head front is unambiguous
- **Close-zoom camera** — `minDistance` 3.0 → 0.4, near plane 0.10 → 0.05, fog start
  28 m → 38 m, per-station camera presets pulled in to (+1.4, 1.6, −2.0)
- **Shoulder-cap geometry** on G1 robot torsos to hide the body-box top edge
- **Z-fight elimination** — opaque coat materials with `polygonOffset:-1`, enlarged coat
  box (0.36 × 0.44 × 0.22) and sleeve capsule (0.052r × 0.16L)
- **Realistic adult leg proportions** for the human patient — thigh & shin lengthened to
  0.42 m each so feet rest on the floor when seated
- **Cross-body inject pose** — shoulder yaw −83°, elbow bend 100°, doctor XOff −0.30,
  ZOff +0.10 so the syringe needle contacts the patient's right deltoid
- **Longer syringe needle** — 0.06 m → 0.10 m for visible contact
- **Brighter injection-target highlight** during inject/hold — emissive intensity 0.4 → 0.9,
  pulse amplitude 0.15 → 0.25, double frequency
- **Six-version nav banner** — clickable links across v0.1.0, v0.5.0, v0.6.0, v0.7.0,
  v0.8.0, v0.9.0 (current)
- **v0.9.0 release notes** in `releases.md`
- **v0.9.0 build prompt** in `prompts.md`

### Changed
- Nav banner in v0.1.0, v0.5.0, v0.6.0, v0.7.0, and v0.8.0 viewers updated to include
  v0.9.0 link
- `pyproject.toml` version from 0.8.0 to 0.9.0
- `simulation_v2/run_competition.py` version string from 0.8.0 to 0.9.0
- `simulation_v2/export_competition.py` version string from 0.8.0 to 0.9.0
- `tests/test_exports.py` to expect version 0.9.0
- README updated with v0.9.0 documentation, version table, and architecture diagrams
- Patient root y lowered 1.15 → 0.775 so the pelvis rests on the cushion
- Patient root z pushed back 0.02 → 0.10 so the torso rests near the backrest
- Patient arm rest pose softened (UpperArm.x 0.30 → 0.18, Elbow.x −0.90 → −1.05)
- Doctor/nurse home y lowered 0.89 → 0.80 so feet stand on the floor
- Station label y lowered 2.4 → 2.0 so it reads well on close-zoom

### Fixed
- **Patient seating (issue #1)**: Patients no longer float above the chair with feet on
  the cushion — pelvis rests on the cushion, feet hit the floor
- **Patient head orientation + facial features (issue #2)**: Head is explicitly
  forward-facing, with eyes/eyebrows/nose/mouth/chin/hair fringe added to disambiguate
- **Close-zoom (issue #3)**: Each station can now be inspected at near-touching range
  via mouse wheel / pinch zoom
- **Shoulder Z-fighting (issue #4)**: Coat overlays use opaque materials with
  `polygonOffset` and fully enclose the body box; the shoulder seam no longer flickers
- **Needle contact (issue #5)**: Doctor's cross-body inject pose plus a longer needle
  ensures the syringe tip contacts the patient's right deltoid during inject and hold

## [0.8.0] — 2026-03-04

### Added
- v0.8.0 competition viewer (`docs/v8/index.html`) — complete visual overhaul
- Premium dark theme (#0d1117 gradient) with frosted glass UI panels and neon cyan accents
- PBR-style materials: specular highlights on G1 bodies, translucent IV bags with fluid level
- Enhanced G1 robots: articulated finger segments, battery pack, spine LED strip, ankle actuators
- Realistic human patients: hospital wristband, pulse oximeter, visible arm veins, individual fingers
- Surgical overhead spotlights with visible glow cones per station quadrant
- Glass observation window, curtain dividers between station pairs
- Emergency exit sign, wall-mounted hand sanitizer dispensers
- Doctor holds alcohol swab in left hand during preparation phase
- Nurse wears stethoscope around neck, pen in coat pocket
- 18m x 18m room with 6.0m grid spacing
- Five-version nav banner: v0.1.0, v0.5.0, v0.6.0, v0.7.0, v0.8.0 (new)
- v0.8.0 release notes in `releases.md`
- v0.8.0 build prompt in `prompts.md`

### Changed
- Nav banners in v0.1.0, v0.5.0, v0.6.0, v0.7.0 updated to include v0.8.0 link
- `pyproject.toml` version from 0.7.0 to 0.8.0
- `simulation_v2/run_competition.py` version string to 0.8.0
- `simulation_v2/export_competition.py` version string to 0.8.0
- `tests/test_exports.py` to expect version 0.8.0
- README updated with v0.8.0 documentation and version table
- @kevinkawchak: Note v0.8.0/v0.7.0 have roofs in main README - 2026-03-04.

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
- @kevinkawchak made a note in main README that v0.7.0 has a roof. 2026-03-04

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
