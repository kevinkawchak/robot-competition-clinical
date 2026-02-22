# Releases

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
- Stations compete on both time (fastest doctor review + nurse injection) and accuracy
  (needle-to-target distance)
- The nurse accuracy is measured as Euclidean distance between needle tip and the marked
  injection site on the patient's right deltoid
- Light mode with white/light backgrounds makes it easy to zoom into each station and
  identify individual robot components and medical equipment

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
