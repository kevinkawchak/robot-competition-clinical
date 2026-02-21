# Releases

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
