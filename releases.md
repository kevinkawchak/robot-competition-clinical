# Releases

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
