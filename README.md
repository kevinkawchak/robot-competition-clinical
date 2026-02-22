# Clinical Robot Competition

MuJoCo-based clinical trial simulation with Unitree G1 humanoid robots competing
across **four simultaneous stations** in a 2x2 grid. Each station replicates the
**v0.1.0 single-station layout**: a **doctor** (white coat, right of patient) performs
a 7-phase deltoid injection with syringe, while a **nurse** (blue coat, left of patient)
monitors the procedure with a tablet. All stations are driven by **PPO reinforcement
learning** policies with distinct behavior profiles from different random seeds.

The building ceiling is removed so viewers can see through the hospital room from above.

Built as the next step beyond [mjlab](https://github.com/mujocolab/mjlab)
(mujocolab/mjlab), extending GPU-accelerated robot simulation into clinical
competition scenarios with universal device accessibility.

## Quick Start (1-2 Steps from GitHub)

**Step 1:** Enable GitHub Pages in your fork:
Settings → Pages → Source: "Deploy from a branch" → Branch: `main`, Folder: `/docs` → Save

**Step 2:** Open the simulation on any device (desktop, iOS, Android):

| Simulation | URL | Description |
|---|---|---|
| **v0.5.0 Competition** | [https://kevinkawchak.github.io/robot-competition-clinical/v5/](https://kevinkawchak.github.io/robot-competition-clinical/v5/) | 4-station PPO competition (light mode, open-top) |
| **v0.1.0 Single Station** | [https://kevinkawchak.github.io/robot-competition-clinical/](https://kevinkawchak.github.io/robot-competition-clinical/) | Original single-station injection (stable) |

Press **Play** to start the competition and watch all 4 stations race. Use the
toggle buttons to open/close the **Phase Timeline** and **Scoreboard** panels.
When all stations finish, a **Competition Results** overlay displays the final
1st/2nd/3rd/4th ranking with times and accuracies. Close the overlay and use
**Reset** to replay.

## What This Simulates (v0.5.0)

Four identical stations compete simultaneously, each replicating the v0.1.0 single-station
layout. Every station uses the same PPO policy architecture but with different random seed
initialization, producing distinct timing and accuracy behavior.

### v0.5.0 Changes from v0.4.0

| Aspect | v0.4.0 | v0.5.0 |
|---|---|---|
| Station layout | Doctor LEFT (tablet), Nurse RIGHT (syringe) | **Doctor RIGHT (syringe), Nurse LEFT (tablet)** — matches v0.1.0 |
| Procedure | 4 doctor review + 6 nurse injection phases | **7 doctor injection phases** — matches v0.1.0 |
| Building | Ceiling present | **No ceiling** — see through from above |
| Humanoids | CylinderGeometry arms, simple groups | **CapsuleGeometry limbs, hierarchical joint groups** — v0.1.0 articulation |
| Nav banner | v0.1.0, v0.3.0, v0.4.0 links | **v0.1.0 and v0.5.0 only** |
| URL path | `/v4/` | **`/v5/`** |

### Station Layout (2x2 Grid)

| Station | Position | Seed | Speed | Accuracy | Profile |
|---------|----------|------|-------|----------|---------|
| **A** | Front-left | 42 | 1.00x | High | Balanced |
| **B** | Front-right | 137 | 0.88x | Medium | Speed-focused |
| **C** | Back-left | 256 | 1.08x | Highest | Accuracy-focused |
| **D** | Back-right | 512 | 0.95x | High | Cautious |

### Role Assignments (v0.1.0 Layout)

| Role | Position | Appearance | Equipment | Action |
|------|----------|------------|-----------|--------|
| Doctor | Right of patient | White coat, red cross | Syringe | Performs 7-phase injection |
| Patient | Center (seated) | Green gown | Exam chair | Receives injection (right arm) |
| Nurse | Left of patient | Blue coat, gold badge | Tablet | Monitors procedure |

### 7-Phase Injection Procedure Per Station (v0.1.0)

All 7 phases are performed by the **doctor** (matching v0.1.0 exactly):

1. **Prepare** — Doctor prepares syringe (1.0s base)
2. **Approach** — Doctor approaches patient from the right (2.0s base)
3. **Position** — Doctor positions needle at right deltoid (1.5s base)
4. **Inject** — Needle insertion at injection target (2.0s base)
5. **Hold** — Steady hold during medication delivery (1.5s base)
6. **Withdraw** — Syringe removal from injection site (1.5s base)
7. **Monitor** — Post-injection monitoring, nurse assists (2.0s base)

**Total base duration:** 11.5 seconds. PPO jitter produces actual times of ~10–14s.

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

- **Time**: Elapsed simulation seconds from prepare phase start to monitor phase end (all 7 phases)
- **Accuracy**: Simulated Euclidean distance (meters) between needle tip and injection target site
- **Accuracy Score**: `1.0 / (1.0 + distance * 100.0)` — higher is better
- **PPO Reward**: Weighted sum of time penalty, accuracy reward, and smoothness reward
- **Ranking**: Stations ranked by total time (lower is better), tiebroken by accuracy score

### Simulation Results (v0.5.0)

Results from `python -m simulation_v2.run_competition`:

| Rank | Station | Total Time | Accuracy | Needle Dist | PPO Reward |
|------|---------|-----------|----------|-------------|------------|
| #1 | **B** | 12.514s | 32.8% | 0.0205m | -3.1064 |
| #2 | D | 13.734s | 50.6% | 0.0098m | -3.4585 |
| #3 | A | 13.810s | 43.6% | 0.0130m | -3.4684 |
| #4 | C | 14.830s | 61.1% | 0.0064m | -3.7605 |

**Winner: Station B** — fastest total time (12.514s) despite lower accuracy, demonstrating
the speed vs. accuracy tradeoff inherent in the PPO reward function.

## Features

- **4-Station Competition**: Simultaneous independent simulation across all stations
- **v0.1.0 Station Layout**: Doctor (right, syringe) performs injection, nurse (left, tablet) monitors
- **7-Phase Procedure**: Matching v0.1.0's exact injection procedure per station
- **PPO RL Policies**: Distinct behavior from seeded policy training
- **Open-Top Building**: No ceiling for unobstructed viewing from above
- **Light-Mode Viewer** (v0.5.0): White/light theme for easy station inspection
- **Articulated Humanoids**: CapsuleGeometry limbs, hierarchical joint groups (shoulder/elbow/wrist)
- **Joint Detail**: Rings at every articulation, visors, role markers (red cross, gold badge)
- **Full Medical Equipment**: IV stand, instrument tray, vitals monitor, exam chair per station
- **Pulsing Injection Marker**: Red dot with animated ring on patient right deltoid
- **Closable Scoreboard**: Toggle on/off — total time, accuracy, needle distance, rank
- **Closable Phase Timeline**: Toggle on/off — tracks all 7 phases per station
- **Competition Results Overlay**: 1st/2nd/3rd/4th display with times and accuracies
- **Metrics Reset**: Full state reset between competition runs
- **Cross-Device 3D Viewer**: Desktop, iOS, Android via Three.js
- **Zero Installation**: View directly from GitHub Pages
- **MuJoCo Physics**: Full MJCF scene models with articulated humanoids
- **Interactive Controls**: Play/pause, reset, station camera focus
- **File Upload**: Upload custom JSON configs for station seeds/speeds
- **Mobile-Optimized**: Responsive layout across iPhone, Android, tablet, desktop
- **Open & Free**: All dependencies open-source (no wandb)

## Architecture Diagrams

### Diagram 1: Multi-Station Competition Architecture (v0.5.0)

```
+----------------------------------------------------------------------+
|        CLINICAL ROBOT COMPETITION - SYSTEM ARCHITECTURE v0.5.0       |
|  4-Station PPO Simulation — v0.1.0 Layout, Open-Top, Light-Mode     |
+----------------------------------------------------------------------+
|                                                                      |
|  +----------------------+        +-------------------------------+   |
|  |  MuJoCo Backend      |        |   Three.js Competition Viewer |   |
|  |  (Python)            |        |   (HTML/JS - docs/v5/)        |   |
|  |                      |        |                               |   |
|  | +------------------+ |  JSON  | +---------------------------+ |   |
|  | | competition_scene| | -----> | | 4-Station 3D Renderer    | |   |
|  | | .xml (4 stations)| | export | | - 2x2 Grid (5.5m space)  | |   |
|  | +------------------+ |        | | - 12 Articulated G1 Bots | |   |
|  |        |             |        | | - CapsuleGeom + joints    | |   |
|  |        v             |        | | - Role markers            | |   |
|  | +------------------+ |        | | - Pulsing inject target   | |   |
|  | | ppo_policy.py    | |        | | - 4x Full Equipment      | |   |
|  | | - PPO MLP 64x64  | |        | | - NO ceiling (see thru)  | |   |
|  | | - 4 seed configs | |        | +---------------------------+ |   |
|  | | - Reward function| |        |          |                    |   |
|  | +------------------+ |        |          v                    |   |
|  |        |             |        | +---------------------------+ |   |
|  |        v             |        | | Per-Station Animation    | |   |
|  | +------------------+ |        | | - 7 doctor phases (v0.1) | |   |
|  | | run_competition  | |        | | - Nurse monitors          | |   |
|  | | .py              | |        | | - Independent timing      | |   |
|  | | - 4 stations     | |        | | - Hierarchical arm anim   | |   |
|  | | - Metrics/rank   | |        | | - Finish-order tracking   | |   |
|  | +------------------+ |        | +---------------------------+ |   |
|  |        |             |        |          |                    |   |
|  |        v             |        |          v                    |   |
|  | +------------------+ |        | +---------------------------+ |   |
|  | | export_competitn | |        | | Light-Mode UI (v0.5.0)   | |   |
|  | | .py              | |        | | - #e8ecf0 background      | |   |
|  | | - Station frames | |        | | - Closable scoreboard     | |   |
|  | | - JSON output    | |        | | - Closable phase timeline | |   |
|  | | - Schema v0.5.0  | |        | | - Results overlay (close) | |   |
|  | +------------------+ |        | | - Metrics reset on replay | |   |
|  |                      |        | | - v0.1.0 + v0.5.0 banner  | |   |
|  +----------------------+        | +---------------------------+ |   |
|                                  +-------------------------------+   |
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

### Diagram 2: PPO Competition Workflow (v0.5.0)

```
+----------------------------------------------------------------------+
|              PPO COMPETITION WORKFLOW - 4-STATION RACE                |
|     v0.5.0: Doctor 7-Phase Injection (matching v0.1.0 procedure)     |
+----------------------------------------------------------------------+
|                                                                      |
|  +--- STATION A (seed=42, balanced, 1.00x speed) ----------------+  |
|  | [prepare][approach][position][inject][hold][withdraw][monitor]  |  |
|  | <-- base 1.0 + 2.0 + 1.5 + 2.0 + 1.5 + 1.5 + 2.0 = 11.5s -> |  |
|  | Actual: ~13.8s (PPO jitter) | Accuracy: 43.6%                 |  |
|  +----------------------------------------------------------------+  |
|  +--- STATION B (seed=137, speed-focused, 0.88x) ----------------+  |
|  | [prepare][approach][position][inject][hold][withdraw][monitor]  |  |
|  | Actual: ~12.5s (FASTEST) | Accuracy: 32.8% (lowest)           |  |
|  +----------------------------------------------------------------+  |
|  +--- STATION C (seed=256, accuracy-focused, 1.08x) -------------+  |
|  | [prepare][approach][position][inject][hold][withdraw][monitor]  |  |
|  | Actual: ~14.8s (slowest) | Accuracy: 61.1% (HIGHEST)          |  |
|  +----------------------------------------------------------------+  |
|  +--- STATION D (seed=512, cautious, 0.95x) ---------------------+  |
|  | [prepare][approach][position][inject][hold][withdraw][monitor]  |  |
|  | Actual: ~13.7s | Accuracy: 50.6%                              |  |
|  +----------------------------------------------------------------+  |
|                                                                      |
|  +--------------- PPO REWARD FUNCTION --------------------------+   |
|  |                                                               |   |
|  |  R = -0.3 x time  +  0.5 / (1 + dist)  +  0.2 / (1 + jerk) |   |
|  |       ^                   ^                    ^              |   |
|  |   Speed penalty     Accuracy reward     Smoothness reward    |   |
|  |                                                               |   |
|  |  Policy: MLP 64x64, tanh | g=0.99 | clip=0.2 | lr=3e-4     |   |
|  |  Same architecture, 4 different seeds -> 4 distinct policies  |   |
|  +---------------------------------------------------------------+   |
|                                                                      |
|  +--------------- COMPETITION RESULTS ----------------------------+  |
|  |   #1  Station B - 12.51s - 32.8% accuracy  (speed wins)      |  |
|  |   #2  Station D - 13.73s - 50.6% accuracy                    |  |
|  |   #3  Station A - 13.81s - 43.6% accuracy                    |  |
|  |   #4  Station C - 14.83s - 61.1% accuracy  (most accurate)   |  |
|  |           [ Close Results ]  <- user manually replays          |  |
|  +----------------------------------------------------------------+  |
+----------------------------------------------------------------------+
```

### Diagram 3: v0.5.0 3D Layout and Technology Stack

```
+----------------------------------------------------------------------+
|      3D LAYOUT & TECHNOLOGY STACK (v0.5.0 — Open-Top Building)       |
+----------------------------------------------------------------------+
|                                                                      |
|  +---------- HOSPITAL ROOM (16m x 16m, NO CEILING) --------------+  |
|  |                    (open top — see through)                    |  |
|  |  +-- Station A --------+    +-- Station B --------+           |  |
|  |  | [Nrs]  [Pat]  [Doc] |    | [Nrs]  [Pat]  [Doc] |           |  |
|  |  |  (L)   chair   (R)  |    |  (L)   chair   (R)  |           |  |
|  |  |  tab   IV+mon  syr  |    |  tab   IV+mon  syr  |           |  |
|  |  |  +     [target]    X |    |  +     [target]    X |           |  |
|  |  +----------------------+    +----------------------+           |  |
|  |        5.5m spacing               5.5m spacing                 |  |
|  |  +-- Station C --------+    +-- Station D --------+           |  |
|  |  | [Nrs]  [Pat]  [Doc] |    | [Nrs]  [Pat]  [Doc] |           |  |
|  |  |  (L)   chair   (R)  |    |  (L)   chair   (R)  |           |  |
|  |  |  tab   IV+mon  syr  |    |  tab   IV+mon  syr  |           |  |
|  |  |  +     [target]    X |    |  +     [target]    X |           |  |
|  |  +----------------------+    +----------------------+           |  |
|  |                                                                |  |
|  |  Legend: X=Doctor(cross,syringe) +=Nurse(badge,tablet)         |  |
|  |  Doc=Doctor(white,R) Pat=Patient(green) Nrs=Nurse(blue,L)     |  |
|  +----------------------------------------------------------------+  |
|                                                                      |
|  LAYER 1: MuJoCo + PPO (Python backend)                             |
|  LAYER 2: Three.js r169 (docs/v5/index.html)                        |
|  LAYER 3: GitHub Pages (static hosting)                              |
|                                                                      |
|  OPEN-SOURCE: MuJoCo(Apache2) Three.js(MIT) Python(PSF) Ruff(MIT)  |
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
│   │   ├── index.html                  # v0.4.0 Competition viewer (legacy)
│   │   └── competition_data.json       # v0.4.0 animation data
│   ├── v5/
│   │   └── index.html                  # v0.5.0 Competition viewer (current)
│   └── diagrams/
│       ├── v1_architecture.md          # Archived v0.1.x text diagrams
│       ├── v2_architecture.md          # Archived v0.2.0 text diagrams
│       ├── v2_viewer_modules.md        # v0.3.0 viewer internal module map
│       ├── v3_architecture.md          # Archived v0.3.0 text diagrams
│       └── v4_architecture.md          # Archived v0.4.0 text diagrams
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

# --- v0.5.0 Competition ---
python -m simulation_v2.run_competition
python -m simulation_v2.export_competition --output docs/v5/competition_data.json

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
