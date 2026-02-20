# Clinical Robot Simulation

MuJoCo-based clinical trial simulation with Unitree G1 humanoid robots performing
cancer medication injection procedures. Built as the next step beyond
[mjlab](https://github.com/mujocolab/mjlab) (mujocolab/mjlab), extending
GPU-accelerated robot simulation into the clinical domain with universal device
accessibility.

## Quick Start (1-2 Steps from GitHub)

**Step 1:** Enable GitHub Pages in your fork:
Settings → Pages → Source: "Deploy from a branch" → Branch: `main`, Folder: `/docs` → Save

**Step 2:** Open the generated URL (e.g., `https://<username>.github.io/robot-competition-clinical/`)
on any device (desktop, iOS, Android).

Press **Play** to watch the injection procedure simulation.

## What This Simulates

Three G1 humanoid robots perform a complete intramuscular (IM) deltoid injection
procedure for cancer immunotherapy medication delivery:

| Role    | Appearance         | Equipment           | Action                            |
|---------|--------------------|---------------------|-----------------------------------|
| Doctor  | White shell, red ✚ | Syringe with needle | Administers injection to deltoid  |
| Nurse   | Blue shell, badge  | Monitoring tablet   | Monitors patient vitals           |
| Patient | Green gown         | Seated in chair     | Receives medication (upper arm)   |

### Injection Procedure Phases

1. **Prepare** — Doctor raises syringe to ready position
2. **Approach** — Doctor moves toward patient's right side
3. **Position** — Syringe aligned with deltoid muscle (upper arm)
4. **Inject** — Needle insertion at 90° angle (standard IM technique)
5. **Hold** — Steady hold during medication delivery
6. **Withdraw** — Syringe removal from injection site
7. **Monitor** — Nurse checks patient post-injection

## Features

- **Cross-Device 3D Viewer**: Works on desktop, iOS, and Android via Three.js
- **Zero Installation**: View directly from GitHub Pages; no terminal needed
- **MuJoCo Physics**: Full MJCF scene model with articulated humanoid robots
- **Interactive Controls**: Play/pause, reset, progress scrubbing, orbit camera
- **File Upload**: Upload custom JSON/XML scene data for future configurations
- **Responsive UI**: Adapts layout for mobile and desktop screens
- **Role Differentiation**: Visual and functional distinction between doctor, nurse, patient
- **Open & Free**: All dependencies and services are fully open-source (no wandb)

## Advances Over mjlab

| Aspect                  | mjlab                         | This Project                        |
|-------------------------|-------------------------------|-------------------------------------|
| Domain                  | General RL locomotion         | Clinical trial procedures           |
| Device Support          | NVIDIA GPU required           | Any device with a web browser       |
| Viewing                 | MuJoCo native / Viser         | Three.js (iOS, Android, desktop)    |
| Installation            | `uv run` / GPU setup          | GitHub Pages (zero install)         |
| Scene Focus             | Velocity tracking, imitation  | Medical injection, patient care     |
| Robot Roles             | Single agent                  | Multi-agent (doctor, nurse, patient)|
| Custom Data             | WandB motion datasets         | File upload (JSON/XML, no wandb)    |

## Architecture Diagrams

### Diagram 1: System Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                    CLINICAL ROBOT SIMULATION                        │
│                         System Architecture                         │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌─────────────────────┐         ┌─────────────────────────────┐   │
│  │   MuJoCo Backend    │         │    Three.js Web Viewer      │   │
│  │   (Python)          │         │    (HTML/JS - docs/)        │   │
│  │                     │         │                             │   │
│  │  ┌───────────────┐  │  JSON   │  ┌───────────────────────┐ │   │
│  │  │ clinical_scene│  │ ──────► │  │  3D Scene Renderer    │ │   │
│  │  │ .xml (MJCF)   │  │ export  │  │  - G1 Humanoid Models │ │   │
│  │  └───────────────┘  │         │  │  - Hospital Room      │ │   │
│  │         │           │         │  │  - Medical Equipment  │ │   │
│  │         ▼           │         │  └───────────────────────┘ │   │
│  │  ┌───────────────┐  │         │           │                │   │
│  │  │ run_simulation│  │         │           ▼                │   │
│  │  │ .py           │  │         │  ┌───────────────────────┐ │   │
│  │  │ - Physics sim │  │         │  │  Animation Engine     │ │   │
│  │  │ - Joint ctrl  │  │         │  │  - 7 Procedure Phases │ │   │
│  │  │ - Contact det │  │         │  │  - Smoothstep Interp  │ │   │
│  │  └───────────────┘  │         │  │  - Keyframe Playback  │ │   │
│  │         │           │         │  └───────────────────────┘ │   │
│  │         ▼           │         │           │                │   │
│  │  ┌───────────────┐  │         │           ▼                │   │
│  │  │ export_anim   │  │         │  ┌───────────────────────┐ │   │
│  │  │ .py           │  │         │  │  UI Controls          │ │   │
│  │  │ - Frame data  │  │         │  │  - Play / Pause       │ │   │
│  │  │ - JSON output │  │         │  │  - Progress Scrub     │ │   │
│  │  └───────────────┘  │         │  │  - File Upload        │ │   │
│  │                     │         │  │  - Info Panel         │ │   │
│  └─────────────────────┘         │  └───────────────────────┘ │   │
│                                  │           │                │   │
│                                  │           ▼                │   │
│  ┌─────────────────────┐         │  ┌───────────────────────┐ │   │
│  │   CI/CD Pipeline    │         │  │  Device Targets       │ │   │
│  │   (GitHub Actions)  │         │  │  ✓ Desktop Browsers   │ │   │
│  │                     │         │  │  ✓ iOS Safari/Chrome  │ │   │
│  │  - ruff lint        │         │  │  ✓ Android Chrome     │ │   │
│  │  - ruff format      │         │  │  ✓ Touch + Mouse      │ │   │
│  │  - Python 3.10-3.12 │         │  └───────────────────────┘ │   │
│  └─────────────────────┘         └─────────────────────────────┘   │
│                                                                     │
│  Attribution: Simulation framework inspired by mjlab                │
│  (mujocolab/mjlab) - Isaac Lab API + MuJoCo Warp                   │
└─────────────────────────────────────────────────────────────────────┘
```

**Benefits**: Dual-path architecture enables physics-accurate MuJoCo simulation
for research while providing zero-install web viewing for accessibility across
all devices. The JSON export bridge connects the two systems.

### Diagram 2: Clinical Injection Workflow

```
┌─────────────────────────────────────────────────────────────────────┐
│              CLINICAL INJECTION PROCEDURE WORKFLOW                   │
│           G1 Humanoid Robot - Deltoid IM Injection                  │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  TIME ──────────────────────────────────────────────────────► 11.5s │
│                                                                     │
│  Phase 1        Phase 2       Phase 3       Phase 4                 │
│  PREPARE        APPROACH      POSITION      INJECT                  │
│  (1.0s)         (2.0s)        (1.5s)        (2.0s)                  │
│  ┌──────┐      ┌──────┐      ┌──────┐      ┌──────┐               │
│  │Doctor│      │Doctor│      │Doctor│      │Doctor│               │
│  │raises│ ───► │walks │ ───► │aligns│ ───► │needle│               │
│  │syring│      │toward│      │needle│      │insert│               │
│  │  e   │      │patnt │      │@ delt│      │ 90°  │               │
│  └──────┘      └──────┘      └──────┘      └──────┘               │
│     │             │             │             │                     │
│     │   Phase 5   │   Phase 6   │  Phase 7   │                     │
│     │   HOLD      │   WITHDRAW  │  MONITOR   │                     │
│     │   (1.5s)    │   (1.5s)    │  (2.0s)    │                     │
│     │  ┌──────┐   │  ┌──────┐   │ ┌──────┐   │                    │
│     │  │Steady│   │  │Remove│   │ │Nurse │   │                    │
│     └─►│ hold │ ──┘─►│needle│ ──┘►│checks│   │                    │
│        │admin │      │from  │     │vitals│   │                    │
│        │ med  │      │ arm  │     │      │   │                    │
│        └──────┘      └──────┘     └──────┘   │                    │
│                                               │                    │
│  PATIENT STATE:   [Seated in exam chair throughout]                │
│  INJECTION SITE:  Right deltoid (lateral upper arm)                │
│  MEDICATION:      Cancer immunotherapy agent                       │
│  TECHNIQUE:       Standard IM injection, 90° angle                 │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────┐       │
│  │ ROBOT ASSIGNMENTS                                       │       │
│  │                                                         │       │
│  │  [Doctor G1]     [Nurse G1]      [Patient G1]          │       │
│  │  White shell     Blue shell      Green gown            │       │
│  │  Red ✚ emblem    Medical badge   Seated pose           │       │
│  │  Syringe         Tablet/monitor  Right arm exposed     │       │
│  │  Active phases:  Active phases:  Passive throughout:   │       │
│  │  1-6 (procedure) 7 (monitoring)  receives injection    │       │
│  └─────────────────────────────────────────────────────────┘       │
└─────────────────────────────────────────────────────────────────────┘
```

**Benefits**: Procedurally accurate 7-phase injection workflow mirrors real
clinical protocol for intramuscular deltoid injections, making this simulation
valuable for training visualization and procedure validation.

### Diagram 3: Technology Stack and Feature Comparison

```
┌─────────────────────────────────────────────────────────────────────┐
│              TECHNOLOGY STACK & FEATURE MAP                          │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  LAYER 1: PHYSICS ENGINE                                            │
│  ┌────────────────────────────────────────────────────────────┐    │
│  │  MuJoCo (Multi-Joint dynamics with Contact)                │    │
│  │  ├── MJCF XML scene definition (clinical_scene.xml)        │    │
│  │  ├── Rigid body dynamics with 9.81 m/s² gravity            │    │
│  │  ├── Position-controlled actuators (12 joint actuators)    │    │
│  │  ├── Contact detection (needle tip ↔ injection site)       │    │
│  │  └── Sensor feedback (needle position, target distance)    │    │
│  │  Benefit: Research-grade physics identical to mjlab         │    │
│  └────────────────────────────────────────────────────────────┘    │
│                          │                                          │
│  LAYER 2: SIMULATION LOGIC                                          │
│  ┌────────────────────────────────────────────────────────────┐    │
│  │  Python Simulation Engine                                  │    │
│  │  ├── 7-phase injection procedure controller                │    │
│  │  ├── Smoothstep interpolation for natural motion           │    │
│  │  ├── Configurable FPS and export resolution                │    │
│  │  ├── JSON animation data export for web viewer             │    │
│  │  └── CLI with --render, --export, --fps options            │    │
│  │  Benefit: Reproducible physics runs, data export pipeline  │    │
│  └────────────────────────────────────────────────────────────┘    │
│                          │                                          │
│  LAYER 3: VISUALIZATION                                             │
│  ┌────────────────────────────────────────────────────────────┐    │
│  │  Three.js r169 Web Viewer (docs/index.html)                │    │
│  │  ├── WebGL 3D rendering with PBR materials                 │    │
│  │  ├── Shadow mapping (PCF soft shadows)                     │    │
│  │  ├── ACES filmic tone mapping                              │    │
│  │  ├── OrbitControls (mouse + touch)                         │    │
│  │  ├── Responsive CSS (mobile-first)                         │    │
│  │  └── Import maps for zero-build ES module loading          │    │
│  │  Benefit: GPU-accelerated 3D on any modern browser         │    │
│  └────────────────────────────────────────────────────────────┘    │
│                          │                                          │
│  LAYER 4: USER INTERFACE                                            │
│  ┌────────────────────────────────────────────────────────────┐    │
│  │  Interactive Controls                                      │    │
│  │  ├── Play / Pause / Reset buttons                          │    │
│  │  ├── Progress bar with click-to-scrub                      │    │
│  │  ├── Real-time phase label and time display                │    │
│  │  ├── Info panel (phase, time, frame, FPS, procedure info)  │    │
│  │  ├── File upload (JSON/XML) for custom scenes              │    │
│  │  └── Role legend (doctor, nurse, patient, injection site)  │    │
│  │  Benefit: Full simulation control without terminal access  │    │
│  └────────────────────────────────────────────────────────────┘    │
│                          │                                          │
│  LAYER 5: DEPLOYMENT                                                │
│  ┌────────────────────────────────────────────────────────────┐    │
│  │  GitHub Pages (Static Hosting)                             │    │
│  │  ├── Zero-cost hosting via GitHub Pages                    │    │
│  │  ├── Single HTML file with CDN dependencies                │    │
│  │  ├── No build step, no bundler, no server required         │    │
│  │  ├── Works on: Desktop, iOS, Android, tablets              │    │
│  │  └── CI/CD: ruff lint + format (Python 3.10/3.11/3.12)    │    │
│  │  Benefit: 1-2 step deployment, universal accessibility     │    │
│  └────────────────────────────────────────────────────────────┘    │
│                                                                     │
│  OPEN-SOURCE STACK (all free, no wandb)                             │
│  ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐          │
│  │MuJoCo  │ │Three.js│ │GitHub  │ │Python  │ │ Ruff   │          │
│  │Apache  │ │  MIT   │ │Actions │ │ PSF    │ │  MIT   │          │
│  │  2.0   │ │        │ │  Free  │ │        │ │        │          │
│  └────────┘ └────────┘ └────────┘ └────────┘ └────────┘          │
└─────────────────────────────────────────────────────────────────────┘
```

**Benefits**: Five-layer architecture cleanly separates physics, logic,
rendering, interaction, and deployment concerns. Every component is open-source
and free, and the web viewer layer enables universal access without requiring
the GPU-dependent physics layer.

## Project Structure

```
robot-competition-clinical/
├── .github/workflows/ci.yml        # Lint/format CI for Python 3.10-3.12
├── docs/
│   └── index.html                   # Three.js web viewer (GitHub Pages)
├── simulation/
│   ├── __init__.py
│   ├── models/
│   │   └── clinical_scene.xml       # MuJoCo MJCF scene definition
│   ├── run_simulation.py            # Python MuJoCo simulation runner
│   └── export_animation.py          # Export animation data to JSON
├── .gitignore
├── LICENSE                          # Apache License 2.0
├── README.md                        # This file
├── changelog.md                     # Version history
├── releases.md                      # Release notes
├── prompts.md                       # Build prompts
└── pyproject.toml                   # Project configuration + ruff settings
```

## Running the Python Simulation (Optional)

The Python backend is optional — the web viewer works independently.

```bash
# Install dependencies
pip install mujoco numpy

# Run simulation and export animation data
python -m simulation.run_simulation --export output/animation.json

# Run with MuJoCo viewer (requires display)
python -m simulation.run_simulation --render

# Export web animation data only
python -m simulation.export_animation --output docs/animation_data.json
```

## Attribution

Simulation framework inspired by [mjlab](https://github.com/mujocolab/mjlab)
(mujocolab/mjlab) — a lightweight framework for GPU-accelerated robot learning
combining Isaac Lab's manager-based API with MuJoCo Warp physics.

**mjlab citation:**
```bibtex
@misc{zakka2026mjlab,
  title={mjlab: A Lightweight Framework for GPU-Accelerated Robot Learning},
  author={Kevin Zakka and Qiayuan Liao and Brent Yi and
          Louis Le Lay and Koushil Sreenath and Pieter Abbeel},
  year={2026},
  eprint={2601.22074},
  archivePrefix={arXiv},
  primaryClass={cs.RO},
  url={https://arxiv.org/abs/2601.22074}
}
```

## License

Apache License 2.0. See [LICENSE](LICENSE) for details.
