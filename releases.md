# Releases

## Clinical Robot Competition - Senior Peer Review Recommendations
v0.2.1 - 2026-02-21

## Summary

v0.2.1 is a review-and-planning release that adds a new senior engineering peer-review artifact for the full repository. The report provides implementation-ready fixes for Claude, with a specific plan to resolve GitHub Pages directory/path usability so either simulation viewer can be run effectively from different directories and fork paths.

## Features

- Added a new peer-review report at `peer-review/v0.2.1-senior-peer-review.md` with prioritized fixes (high/medium/low)
- Added a concrete GitHub Pages path-portability remediation plan for root (`/`) and competition (`/v2/`) viewers
- Added measurable peer-review metrics: file coverage, check counts, issue severity split, estimated implementation effort, and release-readiness scoring
- Added recommendation metrics summarizing runtime, schema/versioning, testing, and maintainability actions to implement next

## Contributors
@kevinkawchak
@codex
@claude

## Notes
- This release does not change simulation runtime logic directly
- Recommended implementation includes adding base-path aware navigation between root and `/v2/` viewers
- Recommended implementation includes version/schema alignment for exported payloads and added boundary tests

---

## Clinical Robot Competition — 4-Station PPO Simulation
v0.2.0 - 2026-02-21

## Summary

v0.2.0 introduces a 4-station clinical robot competition where doctor/patient/nurse teams race simultaneously in a 2x2 grid layout. Each station uses PPO reinforcement learning policies trained with different random seeds, producing distinct timing and accuracy profiles. The doctor (white coat, left side) reviews patient symptoms and toxicities before the nurse (blue coat, right side) performs a deltoid injection to the patient's nearest arm. All station metrics — doctor review time, nurse injection time, total time, and injection accuracy — are accessible through mobile-friendly control buttons. This release also addresses all 7 peer-review recommendations from v0.1.1 and adds unit tests, shared constants, and type-safe data structures.

## Features

- **4-Station Competition Simulation**: Four complete doctor/patient/nurse stations arranged in a 2x2 grid inside a larger hospital room, each with full medical equipment (IV stand, instrument tray, vitals monitor)
- **PPO Reinforcement Learning**: All stations share the same policy architecture (2-layer MLP, 64x64 units, tanh activation) but are trained with different random seeds (42, 137, 256, 512), producing distinct speed/accuracy tradeoffs
- **Doctor Symptom Review**: Doctor (white coat) on the left reviews patient chart, symptoms, and toxicity levels before approving injection — 4 phases (receive, review, assess, approve)
- **Nurse Injection Procedure**: Nurse (blue coat) on the right performs 6-phase deltoid injection (prepare, approach, position, inject, hold, withdraw) to the patient's arm closest to them
- **Competition Scoreboard**: Real-time display of all 4 stations' doctor time, nurse time, total time, injection accuracy score, and ranking — accessible via mobile-friendly control buttons
- **Separate GitHub Pages**: v0.2.0 competition viewer at `/v2/` distinct from v0.1.x single-station viewer at root — both accessible via different URLs
- **Peer Review Fixes**: All critical/high issues resolved — FPS validation, MuJoCo site ID guards, deterministic frame capture, narrow exception handling
- **Shared Constants Module**: Centralized phase timings and TypedDict data structures eliminating code duplication
- **Unit Test Suite**: Comprehensive tests for phase transitions, interpolation, FPS validation, and competition metrics
- **Pre-commit Configuration**: Local ruff hooks matching CI pipeline standards
- **File Upload Support**: Upload custom competition JSON/XML data for future simulations — upload `competition_data.json` (v2) or `animation_data.json` (v1) via the Upload button

## Contributors
@kevinkawchak
@claude
@codex

## Notes
- The v0.1.x single-station simulation (`simulation/`, `docs/index.html`) remains fully intact and unchanged
- The v0.2.0 competition simulation lives in `simulation_v2/` and `docs/v2/index.html`
- GitHub Pages URLs: root (`/`) = v0.1.x single station; `/v2/` = v0.2.0 competition
- PPO reward function: R = -0.3 * time + 0.5 / (1 + distance) + 0.2 / (1 + jerk)
- All 4 stations use identical policy architecture but different initial weights from seeded training
- Time measurement: elapsed simulation seconds from phase start to completion
- Accuracy measurement: Euclidean distance between needle tip and injection target site
- For future simulations, upload JSON files via the Upload button in the web viewer
- Python backend requires `mujoco`, `numpy`; web viewer requires only a modern browser
- Licensed under Apache License 2.0

---

## Clinical Robot Simulation - Peer Review & Release Planning
v0.1.1 - 2026-02-21

## Summary

v0.1.1 adds a comprehensive senior engineering peer review covering simulation runtime safety, maintainability, CI/testing depth, and documentation consistency. This release documents an actionable, prioritized fix plan for the next implementation cycle.

## Features

- Added a dedicated peer-review artifact under `peer-review/` with 14 targeted recommendations grouped by severity
- Added peer-review metrics for file coverage, issue counts, and implementation effort estimates
- Added prioritized implementation order to guide follow-on coding corrections
- Updated release/changelog records to track review-only changes distinctly from production code modifications

## Contributors
@kevinkawchak
@codex
@claude

## Notes
- This release is documentation/process oriented and does not alter runtime simulation behavior directly
- Recommendation focus areas: input validation, MuJoCo ID safety checks, deterministic frame capture, CI/test expansion, and viewer modularization

## Clinical Robot Simulation - Initial Release
v0.1.0 - 2026-02-20

## Summary

First release of the Clinical Robot Simulation platform, introducing MuJoCo-based
physics simulation with Unitree G1 humanoid robots performing clinical trial
procedures. The simulation features a cross-device web viewer built with Three.js
that runs directly from GitHub Pages on desktop, iOS, and Android devices with no
installation required.

This release establishes the next step beyond the mjlab framework
(mujocolab/mjlab) by bringing GPU-accelerated robot simulation into the clinical
domain with universal device accessibility.

## Features

- **G1 Humanoid Robot Clinical Roles**: Three Unitree G1-style robots operating
  as doctor (white shell, red cross emblem), nurse (blue shell, medical badge),
  and patient (green hospital gown), each with articulated limbs and role-specific
  equipment
- **Deltoid IM Injection Procedure**: Full 7-phase animated procedure for
  intramuscular injection to the patient's upper arm (deltoid muscle), the
  standard site for cancer immunotherapy medication delivery
- **Cross-Device Web Viewer**: Interactive 3D viewer built with Three.js that
  runs on desktop browsers, iOS Safari/Chrome, and Android Chrome with touch
  controls, orbit camera, and responsive UI
- **Zero-Install Simulation**: View the simulation in 1-2 steps from GitHub
  using GitHub Pages deployment from the `docs/` folder; no terminal or package
  installation required
- **Play/Pause/Reset Controls**: Full playback controls with progress bar
  scrubbing, real-time phase indicators, and simulation info panel
- **File Upload**: Upload button supporting JSON/XML files for future custom
  scene configurations and animation data
- **MuJoCo MJCF Scene Model**: Complete clinical scene definition with
  hospital room environment, examination chair, IV stand, medical instrument
  tray, and vitals monitor
- **Python Simulation Backend**: Optional MuJoCo physics simulation runner
  with animation export to JSON for the web viewer
- **CI/CD Pipeline**: GitHub Actions workflow with ruff lint and format checks
  across Python 3.10, 3.11, and 3.12

## Contributors
@kevinkawchak

## Notes
- The web viewer works out of the box via GitHub Pages; enable Pages in repo
  Settings (source: deploy from branch, branch: main, folder: /docs)
- The Python simulation backend requires `mujoco` and `numpy` packages and an
  NVIDIA GPU for MuJoCo Warp acceleration
- Simulation framework inspired by [mjlab](https://github.com/mujocolab/mjlab)
  (Isaac Lab API + MuJoCo Warp) by Kevin Zakka et al.
- All services and dependencies used are fully open and free (no wandb)
- Licensed under Apache License 2.0
