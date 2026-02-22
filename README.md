# Clinical Robot Competition

MuJoCo-based clinical trial simulation with Unitree G1 humanoid robots competing
across **four simultaneous stations** in a 2x2 grid. Each station features a
**doctor** (white coat, left) reviewing patient symptoms/toxicities and a **nurse**
(blue coat, right) performing a deltoid injection to the patient's nearest arm,
all driven by **PPO reinforcement learning** policies with distinct behavior
profiles.

Built as the next step beyond [mjlab](https://github.com/mujocolab/mjlab)
(mujocolab/mjlab), extending GPU-accelerated robot simulation into clinical
competition scenarios with universal device accessibility.

## Quick Start (1-2 Steps from GitHub)

**Step 1:** Enable GitHub Pages in your fork:
Settings → Pages → Source: "Deploy from a branch" → Branch: `main`, Folder: `/docs` → Save

**Step 2:** Open the simulation on any device (desktop, iOS, Android):

| Simulation | URL | Description |
|---|---|---|
| **v0.4.0 Competition** | [https://kevinkawchak.github.io/robot-competition-clinical/v4/](https://kevinkawchak.github.io/robot-competition-clinical/v4/) | 4-station PPO competition (light mode) |
| **v0.1.0 Single Station** | [https://kevinkawchak.github.io/robot-competition-clinical/](https://kevinkawchak.github.io/robot-competition-clinical/) | Original single-station injection (stable) |
| **v0.3.0 Competition** | [https://kevinkawchak.github.io/robot-competition-clinical/v2/](https://kevinkawchak.github.io/robot-competition-clinical/v2/) | Legacy 4-station competition (dark mode) |

Press **Play** to start the competition and watch all 4 stations race. Use the
toggle buttons to open/close the **Phase Timeline** and **Scoreboard** panels.
When all stations finish, a **Competition Results** overlay displays the final
1st/2nd/3rd/4th ranking with times and accuracies. Close the overlay and use
**Reset** to replay.

## What This Simulates (v0.4.0)

Four identical doctor/patient/nurse stations compete simultaneously. Each station
uses the same PPO policy architecture but with different random seed
initialization, producing distinct timing and accuracy behavior.

### v0.4.0 Improvements Over v0.3.0

| Aspect | v0.3.0 | v0.4.0 |
|---|---|---|
| Theme | Dark mode (#0f0f1e) | **Light mode (#e8ecf0)** — easier station zoom |
| Robot detail | Simplified (box torso, sphere head) | **Full articulation** (joint rings, visor, pelvis, knee/elbow joints, role markers) |
| Hospital props | Minimal IV, tray, monitor | **Full equipment** (IV with hook+tube+base arms, tray with vials+swabs, monitor with base, chair with armrest supports) |
| Injection marker | Static red dot | **Pulsing ring + center dot** |
| Doctor emblem | None | **Red cross on chest** |
| Nurse emblem | None | **Gold badge on chest** |
| Metrics reset | Metrics persisted between runs | **Full reset on replay** |
| Results overlay | "Close & Replay" (auto-reset) | **"Close Results"** (manual replay via Reset) |
| Room size | 14m x 14m | **16m x 16m** (more space between stations) |
| Grid spacing | 5.0m | **5.5m** |
| Orientation | All face +Z | **All face +Z** (consistent with v0.1.0) |
| URL path | `/v2/` (version mismatch) | **`/v4/`** (matches version) |

### Station Layout (2x2 Grid)

| Station | Position | Seed | Speed | Accuracy | Profile |
|---------|----------|------|-------|----------|---------|
| **A** | Front-left | 42 | 1.00x | High | Balanced |
| **B** | Front-right | 137 | 0.88x | Medium | Speed-focused |
| **C** | Back-left | 256 | 1.08x | Highest | Accuracy-focused |
| **D** | Back-right | 512 | 0.95x | High | Cautious |

### Role Assignments

| Role | Position | Appearance | Equipment | Action |
|------|----------|------------|-----------|--------|
| Doctor | Left of patient | White coat, red cross | Tablet/chart | Reviews symptoms/toxicities |
| Patient | Center (seated) | Green gown | Exam chair | Receives injection (right arm) |
| Nurse | Right of patient | Blue coat, gold badge | Syringe | Performs deltoid injection |

### Phase Flow Per Station

**Doctor Review** (4 phases, ~5.5s base):
1. **Receive Chart** — Doctor receives patient chart (1.0s)
2. **Review Symptoms** — Doctor reviews symptoms on tablet (2.0s)
3. **Assess Toxicity** — Doctor assesses toxicity levels (1.5s)
4. **Approve Injection** — Doctor approves injection (1.0s)

**Nurse Injection** (6 phases, ~8.5s base, starts after doctor approval):
5. **Prepare Syringe** — Nurse prepares syringe (1.0s)
6. **Approach Patient** — Nurse approaches from the right (1.5s)
7. **Position Needle** — Needle aligned with right deltoid (1.5s)
8. **Inject** — Needle insertion at 90 degree angle (2.0s)
9. **Hold Steady** — Steady hold during medication delivery (1.5s)
10. **Withdraw** — Syringe removal from injection site (1.0s)

### PPO Reinforcement Learning Details

All four stations use **Proximal Policy Optimization (PPO)** with:

- **Architecture**: 2-layer MLP (64 hidden units each), tanh activation
- **Observation space**: `[phase_progress, arm_joint_angles, needle_pos, target_pos, elapsed_time]`
- **Action space**: `[shoulder_pitch_delta, elbow_delta, wrist_delta, approach_velocity]`
- **Reward function**: `R = -0.3 * elapsed_time + 0.5 / (1 + needle_dist) + 0.2 / (1 + motion_jerk)`
- **Training**: 500 episodes, gamma=0.99, clip_ratio=0.2, learning_rate=3e-4
- **Key insight**: Same policy architecture + different random seeds produces different learned behaviors

**Same policy, different state**: Each station shares the same MLP architecture and
PPO hyperparameters. The only difference between stations is the random seed used during
training initialization (42, 137, 256, 512). This produces genuinely distinct learned
parameters — different speed/accuracy tradeoffs — from the same reward function. The
PPO reward `R = -0.3*time + 0.5/(1+dist) + 0.2/(1+jerk)` balances three competing
objectives: speed (finish fast), accuracy (needle close to target), and smoothness
(minimal jerk in arm motion).

### Measurement

- **Time**: Elapsed simulation seconds from start to nurse withdrawal completion
- **Accuracy**: Euclidean distance (meters) between needle tip and injection target site
- **Accuracy Score**: `1.0 / (1.0 + distance * 100.0)` — higher is better
- **PPO Reward**: Weighted sum of time penalty, accuracy reward, and smoothness reward
- **Ranking**: Stations ranked by total time (lower is better), tiebroken by accuracy score

## Features

- **4-Station Competition**: Simultaneous independent simulation across all stations
- **PPO RL Policies**: Distinct behavior from seeded policy training
- **Light-Mode Viewer** (v0.4.0): White/light theme for easy zooming into each station
- **Full-Detail Humanoids**: Joint rings, visors, pelvis, articulated arms/legs, role markers
- **Full Medical Equipment**: IV stand (hook, tube, base arms), tray (vials, swabs), monitor (base, LED)
- **Pulsing Injection Marker**: Red dot with animated ring on patient deltoid
- **Closable Scoreboard**: Toggle on/off — doctor time, nurse time, total, accuracy, rank
- **Closable Phase Timeline**: Toggle on/off — tracks each phase per station
- **Competition Results Overlay**: Clear 1st/2nd/3rd/4th display with times and accuracies
- **Metrics Reset**: Full state reset between competition runs
- **Cross-Device 3D Viewer**: Desktop, iOS, Android via Three.js
- **Zero Installation**: View directly from GitHub Pages
- **MuJoCo Physics**: Full MJCF scene models with articulated humanoids
- **Interactive Controls**: Play/pause, reset, station camera focus
- **File Upload**: Upload custom competition_data.json for future simulations
- **Mobile-Optimized**: Responsive layout across iPhone, Android, tablet, desktop
- **Triple Viewers**: Separate GitHub Pages for v0.1.0, v0.3.0, and v0.4.0
- **Open & Free**: All dependencies open-source (no wandb)

## Uploading Custom Simulations

To upload custom data for future simulations:

1. **v0.4.0 Competition**: Generate a `competition_data.json` file using
   `python -m simulation_v2.export_competition --output competition_data.json`
   and upload it via the **Upload** button in the `/v4/` viewer.

2. **v0.1.0 Single Station**: Generate an `animation_data.json` file using
   `python -m simulation.export_animation --output animation_data.json`
   and upload it via the **Upload** button in the root viewer.

The viewer will parse the JSON structure and apply it to the simulation.

## Architecture Diagrams

### Diagram 1: Multi-Station Competition Architecture (v0.4.0)

```
+----------------------------------------------------------------------+
|        CLINICAL ROBOT COMPETITION - SYSTEM ARCHITECTURE v0.4.0       |
|       4-Station PPO Simulation with Light-Mode Full-Detail Viewer    |
+----------------------------------------------------------------------+
|                                                                      |
|  +----------------------+        +-------------------------------+   |
|  |  MuJoCo Backend      |        |   Three.js Competition Viewer |   |
|  |  (Python)            |        |   (HTML/JS - docs/v4/)        |   |
|  |                      |        |                               |   |
|  | +------------------+ |  JSON  | +---------------------------+ |   |
|  | | competition_scene| | -----> | | 4-Station 3D Renderer    | |   |
|  | | .xml (4 stations)| | export | | - 2x2 Grid (5.5m space)  | |   |
|  | +------------------+ |        | | - 12 Full-Detail G1 Bots | |   |
|  |        |             |        | | - Joint rings + visors    | |   |
|  |        v             |        | | - Role markers            | |   |
|  | +------------------+ |        | | - Pulsing inject target   | |   |
|  | | ppo_policy.py    | |        | | - 4x Full Equipment      | |   |
|  | | - PPO MLP 64x64  | |        | +---------------------------+ |   |
|  | | - 4 seed configs | |        |          |                    |   |
|  | | - Reward function| |        |          v                    |   |
|  | +------------------+ |        | +---------------------------+ |   |
|  |        |             |        | | Per-Station Animation    | |   |
|  |        v             |        | | - Doctor review (4 phase) | |   |
|  | +------------------+ |        | | - Nurse inject (6 phase)  | |   |
|  | | run_competition  | |        | | - Independent timing      | |   |
|  | | .py              | |        | | - Finish-order tracking   | |   |
|  | | - 4 stations     | |        | | - Full arm articulation   | |   |
|  | | - Metrics/rank   | |        | +---------------------------+ |   |
|  | +------------------+ |        |          |                    |   |
|  |        |             |        |          v                    |   |
|  |        v             |        | +---------------------------+ |   |
|  | +------------------+ |        | | Light-Mode UI (v0.4.0)   | |   |
|  | | export_competitn | |        | | - #e8ecf0 background      | |   |
|  | | .py              | |        | | - Closable scoreboard     | |   |
|  | | - Station frames | |        | | - Closable phase timeline | |   |
|  | | - JSON output    | |        | | - Results overlay (close) | |   |
|  | | - Schema v0.4.0  | |        | | - Metrics reset on replay | |   |
|  | +------------------+ |        | | - Cross-nav banner        | |   |
|  |                      |        | +---------------------------+ |   |
|  +----------------------+        +-------------------------------+   |
|                                                                      |
|  +----------------------+        +-------------------------------+   |
|  |   CI/CD + Testing    |        | Device Targets               |   |
|  | - ruff lint/format   |        | - Desktop (mouse+kb)         |   |
|  | - pytest (113 tests) |        | - iPhone (touch+pinch)       |   |
|  | - Python 3.10-3.12   |        | - Android (touch+pinch)      |   |
|  | - pre-commit hooks   |        | - Tablet (responsive)        |   |
|  +----------------------+        +-------------------------------+   |
|                                                                      |
|  Attribution: Inspired by mjlab (mujocolab/mjlab)                   |
+----------------------------------------------------------------------+
```

### Diagram 2: PPO Competition Workflow

```
+----------------------------------------------------------------------+
|              PPO COMPETITION WORKFLOW - 4-STATION RACE                |
|              Doctor Review -> Nurse Injection -> Ranking              |
+----------------------------------------------------------------------+
|                                                                      |
|  +--- STATION A (seed=42, balanced) ----------------------------+   |
|  | DOCTOR REVIEW            | NURSE INJECTION                    |   |
|  | [recv][review][assess][ok]|[prep][approach][pos][inject][hold][wd]|
|  | <-- 5.5s base ---------->|<-- 8.5s base ------------------>  |   |
|  +--------------------------------------------------------------|   |
|  +--- STATION B (seed=137, speed-focused) ----------------------+   |
|  | DOCTOR REVIEW          | NURSE INJECTION                      |   |
|  | [recv][review][asses][ok]|[prep][appr][pos][inject][hold][wd] |   |
|  | <-- ~4.8s ------------>|<-- ~7.5s ------------------------>   |   |
|  +--------------------------------------------------------------|   |
|  +--- STATION C (seed=256, accuracy-focused) -------------------+   |
|  | DOCTOR REVIEW              | NURSE INJECTION                  |   |
|  | [recv][review ][assess][ok]|[prep][approach][pos][inj][hold][wd] |
|  | <-- ~5.9s --------------->|<-- ~9.2s ---------------------->  |   |
|  +--------------------------------------------------------------|   |
|  +--- STATION D (seed=512, cautious) ---------------------------+   |
|  | DOCTOR REVIEW            | NURSE INJECTION                    |   |
|  | [recv][review][assess][ok]|[prep][approach][pos][inject][hd][wd] |
|  | <-- ~5.2s ------------->|<-- ~8.1s ----------------------->   |   |
|  +--------------------------------------------------------------|   |
|                                                                      |
|  +--------------- PPO REWARD FUNCTION --------------------------+   |
|  |                                                               |   |
|  |  R = -0.3 x time  +  0.5 / (1 + dist)  +  0.2 / (1 + jerk) |   |
|  |       ^                   ^                    ^              |   |
|  |   Speed penalty     Accuracy reward     Smoothness reward    |   |
|  |                                                               |   |
|  |  Policy: MLP 64x64, tanh | g=0.99 | clip=0.2 | lr=3e-4     |   |
|  |  Same architecture, different seeds -> different behaviors    |   |
|  +---------------------------------------------------------------+   |
|                                                                      |
|  +--------------- COMPETITION RESULTS OVERLAY -------------------+   |
|  |   #1  Station B - 12.3s - 85.2% accuracy                    |   |
|  |   #2  Station D - 13.3s - 88.1% accuracy                    |   |
|  |   #3  Station A - 14.0s - 90.5% accuracy                    |   |
|  |   #4  Station C - 15.1s - 93.8% accuracy                    |   |
|  |           [ Close Results ]  <- user manually replays        |   |
|  +---------------------------------------------------------------+   |
|                                                                      |
|  Note: Exact times vary per run via seeded PPO policy noise.        |
+----------------------------------------------------------------------+
```

### Diagram 3: Full-Detail 3D Layout and Technology Stack

```
+----------------------------------------------------------------------+
|      FULL-DETAIL 3D LAYOUT & TECHNOLOGY STACK (v0.4.0)               |
+----------------------------------------------------------------------+
|                                                                      |
|  +---------------- HOSPITAL ROOM (16m x 16m) -------------------+   |
|  |                                                               |   |
|  |  +-- Station A ------+    +-- Station B ------+              |   |
|  |  | [Doc]  [Pat]  [Nrs]|    | [Doc]  [Pat]  [Nrs]|             |   |
|  |  |  (L)   chair   (R) |    |  (L)   chair   (R) |             |   |
|  |  |  tab   IV+mon  syr |    |  tab   IV+mon  syr |             |   |
|  |  |  +     [target]    B|    |  +     [target]    B|            |   |
|  |  +--------------------+    +--------------------+             |   |
|  |        5.5m spacing             5.5m spacing                  |   |
|  |  +-- Station C ------+    +-- Station D ------+              |   |
|  |  | [Doc]  [Pat]  [Nrs]|    | [Doc]  [Pat]  [Nrs]|             |   |
|  |  |  (L)   chair   (R) |    |  (L)   chair   (R) |             |   |
|  |  |  tab   IV+mon  syr |    |  tab   IV+mon  syr |             |   |
|  |  |  +     [target]    B|    |  +     [target]    B|            |   |
|  |  +--------------------+    +--------------------+             |   |
|  |        5.5m row spacing                                       |   |
|  |  Legend: +=Doctor(cross) B=Nurse(badge) target=pulsing ring  |   |
|  |  Doc=Doctor(white) Pat=Patient(green) Nrs=Nurse(blue)        |   |
|  +---------------------------------------------------------------+   |
|                                                                      |
|  LAYER 1: PHYSICS ENGINE                                             |
|  +------------------------------------------------------------+     |
|  |  MuJoCo (Multi-Joint dynamics with Contact)                |     |
|  |  - 4-station MJCF XML scene (competition_scene.xml)        |     |
|  |  - 48 joint actuators (12 per station x 4)                 |     |
|  |  - 8 contact sensors (needle_tip + target per station)     |     |
|  |  - 0.002s timestep, position-controlled actuators          |     |
|  +------------------------------------------------------------+     |
|                          |                                           |
|  LAYER 2: PPO POLICY LAYER                                           |
|  +------------------------------------------------------------+     |
|  |  Proximal Policy Optimization (PPO)                        |     |
|  |  - MLP 64x64 with tanh activation (per station)            |     |
|  |  - 4 seeds: 42, 137, 256, 512 -> 4 distinct policies      |     |
|  |  - Reward: speed (-0.3) + accuracy (0.5) + smooth (0.2)    |     |
|  |  - Observation: phase, joints, needle pos, target, time     |     |
|  |  - Action: shoulder/elbow/wrist deltas, approach velocity   |     |
|  +------------------------------------------------------------+     |
|                          |                                           |
|  LAYER 3: VISUALIZATION (v0.4.0 - Light Mode)                       |
|  +------------------------------------------------------------+     |
|  |  Three.js r169 Competition Viewer (docs/v4/index.html)     |     |
|  |  - 12 full-detail G1 humanoid robots (3 per station)       |     |
|  |  - Joint rings, visors, pelvis, articulated arms/legs      |     |
|  |  - Role markers: red cross (doctor), gold badge (nurse)    |     |
|  |  - Pulsing injection target (ring + center dot)            |     |
|  |  - Light theme (#e8ecf0), ACES filmic, PCF shadows         |     |
|  |  - Closable scoreboard + closable phase timeline           |     |
|  |  - Results overlay (close only - manual replay)            |     |
|  |  - Full metrics reset between competition runs             |     |
|  |  - Responsive: iPhone, Android, tablet, desktop            |     |
|  +------------------------------------------------------------+     |
|                          |                                           |
|  LAYER 4: DEPLOYMENT & TESTING                                       |
|  +------------------------------------------------------------+     |
|  |  GitHub Pages + CI Pipeline                                |     |
|  |  - /docs/index.html -> v0.1.0 single station (stable)     |     |
|  |  - /docs/v2/index.html -> v0.3.0 competition (legacy)     |     |
|  |  - /docs/v4/index.html -> v0.4.0 competition (current)    |     |
|  |  - ruff lint + format (Python 3.10/3.11/3.12)              |     |
|  |  - pytest (113 tests)                                      |     |
|  |  - pre-commit hooks for local development                  |     |
|  +------------------------------------------------------------+     |
|                                                                      |
|  OPEN-SOURCE STACK (all free, no wandb)                              |
|  MuJoCo(Apache2) Three.js(MIT) GitHub(Free) Python(PSF) Ruff(MIT)  |
+----------------------------------------------------------------------+
```

## Project Structure

```
robot-competition-clinical/
├── .github/workflows/ci.yml           # Lint/format CI for Python 3.10-3.12
├── .pre-commit-config.yaml            # Local ruff hooks
├── docs/
│   ├── index.html                      # v0.1.0 Three.js viewer (GitHub Pages)
│   ├── v2/
│   │   └── index.html                  # v0.3.0 Competition viewer (legacy)
│   ├── v4/
│   │   └── index.html                  # v0.4.0 Competition viewer (current)
│   └── diagrams/
│       ├── v1_architecture.md          # Archived v0.1.x text diagrams
│       ├── v2_architecture.md          # Archived v0.2.0 text diagrams
│       ├── v2_viewer_modules.md        # v0.3.0 viewer internal module map
│       └── v3_architecture.md          # Archived v0.3.0 text diagrams
├── simulation/                         # v0.1.x single-station simulation
│   ├── __init__.py
│   ├── constants.py
│   ├── models/clinical_scene.xml
│   ├── run_simulation.py
│   └── export_animation.py
├── simulation_v2/                      # v0.2+ competition simulation
│   ├── __init__.py
│   ├── constants.py
│   ├── ppo_policy.py
│   ├── run_competition.py
│   ├── export_competition.py
│   └── models/competition_scene.xml
├── tests/
│   ├── __init__.py
│   ├── test_phases.py
│   ├── test_interpolation.py
│   ├── test_competition.py
│   └── test_exports.py
├── peer-review/
│   ├── v0.1.1-senior-peer-review.md
│   ├── v0.2.1-senior-peer-review.md
│   └── v0.3.0-implementation-report.md
├── .gitignore
├── LICENSE
├── README.md
├── changelog.md
├── releases.md
├── prompts.md
└── pyproject.toml
```

## Running the Python Simulation (Optional)

The Python backend is optional — the web viewers work independently.

```bash
# Install dependencies
pip install mujoco numpy

# --- v0.4.0 Competition ---
python -m simulation_v2.run_competition
python -m simulation_v2.export_competition --output docs/v4/competition_data.json

# --- v0.1.0 Single Station ---
python -m simulation.run_simulation --export output/animation.json
python -m simulation.export_animation --output docs/animation_data.json
```

## Running Tests and Linting

```bash
pip install pytest ruff

# Run all tests (113 tests)
pytest tests/ -v

# Lint check
ruff check .

# Format check
ruff format --check .
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
