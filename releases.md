# Releases

## Clinical Robot Competition — v0.8.0 SOTA G1 Robots & Realistic Patients

v0.8.0 — 2026-03-04

### Summary

Complete visual overhaul introducing a premium dark theme with SOTA Unitree G1 humanoid robots
and highly realistic human patients. The simulation is redesigned from the ground up with a deep
navy/charcoal gradient background (#0d1117), frosted glass UI panels, neon cyan (#00d4ff) accent
colors, and PBR-style materials. The hospital environment now features surgical overhead spotlights
with visible glow cones per station, a glass observation window, medical curtain dividers between
station pairs, emergency exit sign, and wall-mounted hand sanitizer dispensers. G1 robots gain
articulated finger segments (3 fingers with 2 joints each), battery pack on back, spine LED strip,
and ankle actuator housings. Human patients now have hospital wristbands, pulse oximeters, visible
arm veins on the injection arm, and individual finger geometry. The doctor holds an alcohol swab in
the other hand during the preparation phase. The nurse wears a stethoscope draped around the neck
with a pen in the coat pocket. The room is expanded to 18m x 18m with 6.0m grid spacing.

### Features

- Premium dark theme (#0d1117 gradient) with frosted glass UI panels and neon cyan accents
- PBR-style materials: specular highlights on G1 bodies, translucent IV bags with fluid level
- Enhanced G1 robots: articulated finger segments, battery pack, spine LED strip, ankle actuators
- Realistic human patients: hospital wristband, pulse oximeter, visible arm veins, individual fingers
- Surgical overhead spotlights with visible glow cones per station quadrant
- Glass observation window on one wall, curtain dividers between station pairs
- Emergency exit sign, wall-mounted hand sanitizer dispensers
- Doctor holds alcohol swab in left hand during preparation phase
- Nurse wears stethoscope around neck, pen in coat pocket
- 18m x 18m room with 6.0m grid spacing (expanded from 16m/5.5m)
- Five-version nav banner: v0.1.0 | v0.5.0 | v0.6.0 | v0.7.0 | v0.8.0 (new)
- Cross-device support: desktop, iPhone, Android, tablet

### Contributors
@kevinkawchak
@claude

### Notes

- All competition mechanics, scoring, and PPO policies unchanged from v0.7.0
- v0.7.0 and all prior viewers preserved and accessible via nav banner
- Completely new visual design — does not look or behave like any prior version
- Dark premium theme chosen for immersive surgical environment atmosphere

---

## Clinical Robot Competition — v0.7.0 Enhanced Hospital Visuals

v0.7.0 — 2026-03-04

### Summary

Visual and environment upgrade building on v0.6.0's realistic Unitree G1 robots and human patient.
The hospital environment now features a ceiling with light fixtures over each station quadrant,
baseboards along all walls, and a wooden door with frame and handle. The human patient gains
facial features (eyes with pupils, eyebrows, nose, mouth). The G1 robot torso is segmented into
chest and abdomen sections with a metallic seam joint. The nurse G1 robot is now animated
throughout all 7 phases (not just monitoring) with tablet checking, head tracking, and arm
movement. The patient reacts during injection by turning toward the doctor and gripping the
armrest. Both doctor and nurse G1 robots have pulsing LED visor masks. Tone mapping exposure
increased for improved lighting with ceiling glow panels. The objective is to illustrate that
competitions across multiple autonomous robots can make future fully autonomous physical AI
oncology trials faster than current human trials.

### Features

- Enhanced hospital environment: ceiling, light fixtures per quadrant, baseboards, wooden door
- Patient facial features: eyes, pupils, eyebrows, nose, mouth
- G1 torso segmentation: chest/abdomen split with metallic seam joint
- Active nurse animation throughout all 7 injection phases
- Patient reactive animation during injection (head turn, hand grip)
- Nurse G1 LED visor mask pulse (offset frequency from doctor)
- Increased tone mapping exposure (1.5) with ceiling light glow panels
- Four-version nav banner: v0.1.0 | v0.5.0 | v0.6.0 | v0.7.0 (current)
- All v0.6.0 competition mechanics preserved: PPO policies, 4 stations, same scoring
- Cross-device support: desktop, iPhone, Android, tablet

### Contributors
@kevinkawchak
@claude

### Notes

- All competition mechanics, scoring, and PPO policies unchanged from v0.6.0
- v0.6.0 viewer preserved and accessible via nav banner
- Hospital environment additions are lightweight (minimal geometry count impact)

---

## Clinical Robot Competition — v0.6.0 Realistic Unitree G1 Robots & Human Patient

v0.6.0 — 2026-03-03

### Summary

Major visual and accuracy upgrade introducing realistic Unitree G1 humanoid robots (from
unitreerobotics) as the doctor and nurse at each competition station, paired with a realistic
human patient model. The G1 robots feature dark charcoal body panels, glossy black visor heads,
metallic silver joints, and three-fingered dexterous hands matching the real G1's industrial
design (1.32m tall, 23–43 DOF). The patient is now a properly proportioned human figure with
skin-colored anatomy, hair, arms resting on armrests, and correct forward-facing seated
orientation. The injection target marker is placed directly on the patient's right deltoid.
Doctor robot firmly grips the syringe in its dexterous hand. Station labels are lowered to
appropriate height. All animations are smoother with finer interpolation. The objective is to
illustrate that competitions across multiple autonomous robots can make future fully autonomous
physical AI oncology trials faster than current human trials.

### Features

- Realistic Unitree G1 humanoid robot models (unitreerobotics) for doctors and nurses
- G1 design: dark charcoal body, glossy black visor head, metallic silver joints, Dex3-1 hands
- Doctor G1 wears semi-transparent white medical coat overlay + red cross emblem, holds syringe
- Nurse G1 wears semi-transparent blue medical coat overlay + gold badge, holds tablet
- Realistic human patient: skin-colored body, hair, arms, green hospital gown, proper posture
- Patient seated correctly facing forward, arms on armrests, legs in front of chair
- Injection target placed directly on patient's right deltoid (upper arm surface)
- Smoother robot animations with finer interpolation throughout 7-phase procedure
- Station labels lowered closer to participants (y=2.4 vs y=3.2)
- Three-version nav banner: v0.1.0 | v0.5.0 | v0.6.0 (current)
- All v0.5.0 competition mechanics preserved: PPO policies, 4 stations, same scoring
- Light-mode theme with competition scoreboard, phase timeline, results overlay
- Cross-device support: desktop, iPhone, Android, tablet
- Archived v0.5.0 diagrams in docs/diagrams/v5_architecture.md

### Contributors
@kevinkawchak
@claude

### Notes

- The v0.6.0 viewer is at `/v6/` on GitHub Pages
- All four stations use the **same PPO policy architecture** (MLP 64x64, tanh activation)
  but with **different random seeds** (42, 137, 256, 512), producing distinct timing profiles
- **Same policy, different state**: Each station's 7-phase durations are jittered by its
  unique seed. The PPO reward R = -0.3*time + 0.5/(1+dist) + 0.2/(1+jerk) balances speed,
  accuracy, and smoothness — all stations optimize the same reward but converge to different
  local optima due to different initialization
- **Time measurement**: Total elapsed seconds from the start of the prepare phase through
  the end of the monitor phase (all 7 phases summed)
- **Accuracy measurement**: Simulated Euclidean distance between needle tip and injection
  target on patient's right deltoid. Accuracy score = 1/(1+distance*100)
- **Ranking**: By total time (ascending), tiebroken by accuracy score (descending)
- Simulation results (from `python -m simulation_v2.run_competition`):
  - Station A: 13.810s, 43.6% accuracy, rank #3
  - Station B: 12.514s, 32.8% accuracy, rank #1 (WINNER)
  - Station C: 14.830s, 61.1% accuracy, rank #4
  - Station D: 13.734s, 50.6% accuracy, rank #2
- **Unitree G1 reference**: The G1 by unitreerobotics is a 1.32m tall, 35kg humanoid robot
  with 23–43 DOF, dark body panels, visor head, and optional Dex3-1 three-fingered hands.
  See https://www.unitree.com/g1/
- **Why robot competitions for oncology**: Having multiple autonomous G1 robots compete
  simultaneously on injection procedures demonstrates that parallel robot trials can
  accelerate clinical workflows compared to sequential human trials

---

## Clinical Robot Competition — v0.5.0 Open-Top 4-Station Competition

v0.5.0 — 2026-02-22

### Summary

Major update restoring v0.1.0's exact station layout across all four competition stations.
The doctor now performs the injection (syringe in hand, right of patient) while the nurse
monitors (tablet, left of patient), matching the original v0.1.0 single-station design.
Building ceiling removed for see-through viewing. Full v0.1.0 articulated humanoid robots
with hierarchical joint groups (shoulder/elbow/wrist pivots), CapsuleGeometry limbs, joint
rings, and the original 7-phase injection procedure. All four stations compete simultaneously
with PPO reinforcement learning policies using different random seeds.

### Features

- Open-top building (ceiling removed) for unobstructed overhead viewing
- v0.1.0 exact station layout replicated 4 times: doctor (right, syringe), nurse (left, tablet)
- v0.1.0 articulated humanoids with full joint hierarchy enabling realistic animation
- v0.1.0 7-phase procedure: prepare, approach, position, inject, hold, withdraw, monitor
- Full medical equipment per station: IV stand, instrument tray, vitals monitor, exam chair
- Light-mode theme (#e8ecf0) with competition scoreboard, phase timeline, results overlay
- PPO policies (MLP 64x64, tanh) with 4 unique seeds (42, 137, 256, 512)
- Reward: R = -0.3*time + 0.5/(1+dist) + 0.2/(1+jerk)
- Nav banner links only v0.1.0 and v0.5.0
- Archived v0.4.0 diagrams in docs/diagrams/v4_architecture.md

### Contributors
@kevinkawchak
@claude
@codex

### Notes

- The v0.5.0 viewer is at `/v5/` on GitHub Pages
- All four stations use the **same PPO policy architecture** (MLP 64x64, tanh activation)
  but with **different random seeds** (42, 137, 256, 512), producing distinct timing profiles
- **Same policy, different state**: Each station's 7-phase durations are jittered by its
  unique seed. The PPO reward R = -0.3*time + 0.5/(1+dist) + 0.2/(1+jerk) balances speed,
  accuracy, and smoothness — all stations optimize the same reward but converge to different
  local optima due to different initialization
- **Time measurement**: Total elapsed seconds from the start of the prepare phase through
  the end of the monitor phase (all 7 phases summed)
- **Accuracy measurement**: Simulated Euclidean distance between needle tip and injection
  target on patient's right deltoid. Accuracy score = 1/(1+distance*100)
- **Ranking**: By total time (ascending), tiebroken by accuracy score (descending)
- Simulation results (from `python -m simulation_v2.run_competition`):
  - Station A: 13.810s, 43.6% accuracy, rank #3
  - Station B: 12.514s, 32.8% accuracy, rank #1 (WINNER)
  - Station C: 14.830s, 61.1% accuracy, rank #4
  - Station D: 13.734s, 50.6% accuracy, rank #2

---

## Clinical Robot Competition — v0.4.0 Light-Mode Full-Detail Competition

v0.4.0 — 2026-02-22

### Summary

Major viewer upgrade introducing light-mode visualization with full-detail G1 humanoid
robots matching v0.1.0 articulation quality. Fixes metrics persistence bug, GitHub Pages
version/path mismatch, and results overlay auto-replay behavior. Adds role markers,
pulsing injection target, and comprehensive medical equipment to all four competition
stations. Served at `/v4/` path to eliminate the v0.3.0 `/v2/` version mismatch.

### Features

- Light-mode theme (#e8ecf0 background) for easier zooming into individual stations
- Full-detail G1 humanoids: joint rings, visors, pelvis, articulated arms/legs, hands
- Role markers: red cross on doctor, gold badge on nurse
- Pulsing injection target ring with center dot on patient right deltoid
- Full medical equipment: IV stand (hook, tube, 3-arm base), instrument tray (vials,
  spare syringe, swab), monitor (base, screen, LED), exam chair (armrest supports)
- Metrics fully reset between competition runs
- Results overlay shows "Close Results" (user manually replays via Reset)
- 16m x 16m hospital room with 5.5m grid spacing
- Cross-nav banner: v0.1.0 (stable) and v0.4.0 (current)
- Archived v0.3.0 diagrams in docs/diagrams/v3_architecture.md
- Updated all documentation: README, changelog, releases, prompts

### Contributors
@kevinkawchak
@claude
@codex

### Notes

- The v0.4.0 viewer is at `/v4/` (not `/v2/` like v0.3.0) to fix the version mismatch
- All four stations use the same PPO policy architecture (MLP 64x64, tanh) with different
  random seeds (42, 137, 256, 512), producing distinct speed/accuracy behavior profiles
- The PPO reward function R = -0.3*time + 0.5/(1+dist) + 0.2/(1+jerk) balances speed,
  accuracy, and smoothness
- Light mode with white/light backgrounds makes it easy to zoom into each station

---

## Clinical Robot Competition — v0.3.0 Peer Review Implementation

v0.3.0 — 2025-12-15

### Summary

Peer review implementation for the 4-station PPO competition viewer, addressing 10
senior-level recommendations. Adds closable scoreboard and phase timeline, final
results overlay, station selector with camera transitions, and cross-viewer
navigation between v0.1.x and v0.3.0 viewers.

### Features

- Closable scoreboard panel with per-station metrics and rankings
- Closable phase timeline panel tracking doctor and nurse phases
- Final results overlay displaying 1st/2nd/3rd/4th finish order
- Station selector with smooth camera transitions (Overview/A/B/C/D)
- Cross-viewer navigation banner linking v0.1.x and v0.3.0 viewers
- JSON upload with schema validation for custom station configurations
- Export boundary tests for payload correctness
- Internal module map documentation (v2_viewer_modules.md)

### Contributors
@kevinkawchak
@claude
@codex

### Notes

- Dark theme (#0f0f1e) with simplified humanoid models
- Viewer served at `/v2/` path (version mismatch fixed in v0.4.0)
