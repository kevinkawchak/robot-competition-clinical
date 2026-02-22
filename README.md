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
| **v0.3.0 Competition** | [https://kevinkawchak.github.io/robot-competition-clinical/v2/](https://kevinkawchak.github.io/robot-competition-clinical/v2/) | 4-station PPO competition |
| **v0.1.x Single Station** | [https://kevinkawchak.github.io/robot-competition-clinical/](https://kevinkawchak.github.io/robot-competition-clinical/) | Original single-station injection |

Press **Play** to start the competition and watch all 4 stations race. Use the
toggle buttons to open/close the **Phase Timeline** and **Scoreboard** panels.
When all stations finish, a **Competition Results** overlay displays the final
1st/2nd/3rd/4th ranking with times and accuracies.

## What This Simulates (v0.3.0)

Four identical doctor/patient/nurse stations compete simultaneously. Each station
uses the same PPO policy architecture but with different random seed
initialization, producing distinct timing and accuracy behavior.

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
| Doctor | Left of patient | White coat | Tablet/chart | Reviews symptoms/toxicities |
| Patient | Center (seated) | Green gown | Exam chair | Receives injection (right arm) |
| Nurse | Right of patient | Blue coat | Syringe | Performs deltoid injection |

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
8. **Inject** — Needle insertion at 90° angle (2.0s)
9. **Hold Steady** — Steady hold during medication delivery (1.5s)
10. **Withdraw** — Syringe removal from injection site (1.0s)

### PPO Reinforcement Learning Details

All four stations use **Proximal Policy Optimization (PPO)** with:

- **Architecture**: 2-layer MLP (64 hidden units each), tanh activation
- **Observation space**: `[phase_progress, arm_joint_angles, needle_pos, target_pos, elapsed_time]`
- **Action space**: `[shoulder_pitch_delta, elbow_delta, wrist_delta, approach_velocity]`
- **Reward function**: `R = -0.3 * elapsed_time + 0.5 / (1 + needle_dist) + 0.2 / (1 + motion_jerk)`
- **Training**: 500 episodes, gamma=0.99, clip_ratio=0.2, learning_rate=3e-4
- **Key insight**: Same policy architecture + different random seeds → different learned behaviors

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
- **Closable Scoreboard**: Toggle on/off — doctor time, nurse time, total, accuracy, rank
- **Closable Phase Timeline**: Toggle on/off — tracks each phase per station
- **Final Results Overlay**: Clear 1st/2nd/3rd/4th display with times and accuracies
- **Cross-Device 3D Viewer**: Desktop, iOS, Android via Three.js
- **Zero Installation**: View directly from GitHub Pages
- **MuJoCo Physics**: Full MJCF scene models with articulated humanoids
- **Interactive Controls**: Play/pause, reset, station camera focus
- **File Upload**: Upload custom competition_data.json for future simulations
- **Mobile-Optimized**: Responsive layout across iPhone, Android, tablet, desktop
- **Dual Viewers**: Separate GitHub Pages for v1 and v2 with cross-navigation banner
- **Injection Target Marker**: Red marker on patient's deltoid shows needle target
- **Open & Free**: All dependencies open-source (no wandb)

## Uploading Custom Simulations

To upload custom data for future simulations:

1. **v0.3.0 Competition**: Generate a `competition_data.json` file using
   `python -m simulation_v2.export_competition --output competition_data.json`
   and upload it via the **Upload** button in the `/v2/` viewer.

2. **v0.1.x Single Station**: Generate an `animation_data.json` file using
   `python -m simulation.export_animation --output animation_data.json`
   and upload it via the **Upload** button in the root viewer.

The viewer will parse the JSON structure and apply it to the simulation.

## Architecture Diagrams

### Diagram 1: Multi-Station Competition Architecture (v0.3.0)

```
┌──────────────────────────────────────────────────────────────────────┐
│        CLINICAL ROBOT COMPETITION — SYSTEM ARCHITECTURE v0.3.0       │
│          4-Station PPO Simulation with Closable UI Panels            │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌──────────────────────┐        ┌───────────────────────────────┐  │
│  │  MuJoCo Backend      │        │   Three.js Competition Viewer │  │
│  │  (Python)            │        │   (HTML/JS - docs/v2/)        │  │
│  │                      │        │                               │  │
│  │ ┌──────────────────┐ │  JSON  │ ┌───────────────────────────┐│  │
│  │ │ competition_scene│ │ ─────► │ │ 4-Station 3D Renderer    ││  │
│  │ │ .xml (4 stations)│ │ export │ │ - 2x2 Grid (5m spacing)  ││  │
│  │ └──────────────────┘ │        │ │ - 12 G1 Humanoid Models  ││  │
│  │        │             │        │ │ - 4x Medical Equipment   ││  │
│  │        ▼             │        │ │ - Injection target marker ││  │
│  │ ┌──────────────────┐ │        │ └───────────────────────────┘│  │
│  │ │ ppo_policy.py    │ │        │          │                    │  │
│  │ │ - PPO MLP 64x64  │ │        │          ▼                    │  │
│  │ │ - 4 seed configs │ │        │ ┌───────────────────────────┐│  │
│  │ │ - Reward function│ │        │ │ Per-Station Animation    ││  │
│  │ └──────────────────┘ │        │ │ - Doctor review (4 phase) ││  │
│  │        │             │        │ │ - Nurse inject (6 phase)  ││  │
│  │        ▼             │        │ │ - Independent timing      ││  │
│  │ ┌──────────────────┐ │        │ │ - Finish-order tracking   ││  │
│  │ │ run_competition  │ │        │ └───────────────────────────┘│  │
│  │ │ .py              │ │        │          │                    │  │
│  │ │ - 4 stations     │ │        │          ▼                    │  │
│  │ │ - Metrics/rank   │ │        │ ┌───────────────────────────┐│  │
│  │ └──────────────────┘ │        │ │ Competition UI (v0.3.0)  ││  │
│  │        │             │        │ │ - Closable scoreboard     ││  │
│  │        ▼             │        │ │ - Closable phase timeline ││  │
│  │ ┌──────────────────┐ │        │ │ - Final results overlay   ││  │
│  │ │ export_competitn │ │        │ │ - Cross-nav banner        ││  │
│  │ │ .py              │ │        │ │ - Station selector A-D    ││  │
│  │ │ - Station frames │ │        │ │ - JSON upload validation  ││  │
│  │ │ - JSON output    │ │        │ └───────────────────────────┘│  │
│  │ │ - Schema v0.3.0  │ │        │          │                    │  │
│  │ └──────────────────┘ │        │          ▼                    │  │
│  │                      │        │ ┌───────────────────────────┐│  │
│  │                      │        │ │ Device Targets           ││  │
│  └──────────────────────┘        │ │ ✓ Desktop (mouse+kb)     ││  │
│                                  │ │ ✓ iPhone (touch+pinch)   ││  │
│  ┌──────────────────────┐        │ │ ✓ Android (touch+pinch)  ││  │
│  │   CI/CD + Testing    │        │ │ ✓ Tablet (responsive)    ││  │
│  │ - ruff lint/format   │        │ └───────────────────────────┘│  │
│  │ - pytest (113 tests) │        └───────────────────────────────┘  │
│  │ - Python 3.10-3.12   │                                           │
│  │ - export boundary    │     ┌───────────────────────────────┐    │
│  │   tests              │     │  v0.1.x Single-Station Viewer │    │
│  │ - pre-commit hooks   │     │  (docs/index.html — separate) │    │
│  └──────────────────────┘     └───────────────────────────────┘    │
│                                                                      │
│  Attribution: Inspired by mjlab (mujocolab/mjlab)                   │
└──────────────────────────────────────────────────────────────────────┘
```

**Benefits**: Dual-viewer architecture provides both single-station and
competition experiences via separate GitHub Pages URLs with cross-navigation.
Closable panels prevent UI overlap on all devices. The PPO policy layer
enables distinct per-station behaviors from a single codebase. JSON export
bridges MuJoCo physics with zero-install web viewing on any device.

### Diagram 2: PPO Competition Workflow

```
┌──────────────────────────────────────────────────────────────────────┐
│              PPO COMPETITION WORKFLOW — 4-STATION RACE               │
│              Doctor Review → Nurse Injection → Ranking               │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌─── STATION A (seed=42, balanced) ────────────────────────────┐   │
│  │ DOCTOR REVIEW            │ NURSE INJECTION                    │   │
│  │ [recv][review][assess][ok]│[prep][approach][pos][inject][hold][wd]│
│  │ ◄── 5.5s base ──────────►│◄── 8.5s base ────────────────────►│   │
│  └──────────────────────────────────────────────────────────────-┘   │
│  ┌─── STATION B (seed=137, speed-focused) ─────────────────────-┐   │
│  │ DOCTOR REVIEW          │ NURSE INJECTION                      │   │
│  │ [recv][review][asses][ok]│[prep][appr][pos][inject][hold][wd] │   │
│  │ ◄── ~4.8s ────────────►│◄── ~7.5s ──────────────────────────►│   │
│  └──────────────────────────────────────────────────────────────-┘   │
│  ┌─── STATION C (seed=256, accuracy-focused) ──────────────────-┐   │
│  │ DOCTOR REVIEW              │ NURSE INJECTION                  │   │
│  │ [recv][review ][assess][ok] │[prep][approach][pos][inj][hold][wd]│
│  │ ◄── ~5.9s ────────────────►│◄── ~9.2s ──────────────────────►│   │
│  └──────────────────────────────────────────────────────────────-┘   │
│  ┌─── STATION D (seed=512, cautious) ──────────────────────────-┐   │
│  │ DOCTOR REVIEW            │ NURSE INJECTION                    │   │
│  │ [recv][review][assess][ok]│[prep][approach][pos][inject][hd][wd] │
│  │ ◄── ~5.2s ──────────────►│◄── ~8.1s ────────────────────────►│   │
│  └──────────────────────────────────────────────────────────────-┘   │
│                                                                      │
│  ┌──────────────── PPO REWARD FUNCTION ──────────────────────-──┐   │
│  │                                                               │   │
│  │  R = -0.3 × time  +  0.5 / (1 + dist)  +  0.2 / (1 + jerk) │   │
│  │       ▲                   ▲                    ▲              │   │
│  │   Speed penalty     Accuracy reward     Smoothness reward    │   │
│  │                                                               │   │
│  │  Policy: MLP 64×64, tanh | γ=0.99 | clip=0.2 | lr=3e-4     │   │
│  │  Same architecture, different seeds → different behaviors    │   │
│  └───────────────────────────────────────────────────────────────┘   │
│                                                                      │
│  ┌──────────────── FINAL RESULTS DISPLAY ────────────────────-──┐   │
│  │   #1  Station B — 12.3s — 85.2% accuracy                    │   │
│  │   #2  Station D — 13.3s — 88.1% accuracy                    │   │
│  │   #3  Station A — 14.0s — 90.5% accuracy                    │   │
│  │   #4  Station C — 15.1s — 93.8% accuracy                    │   │
│  └───────────────────────────────────────────────────────────────┘   │
│                                                                      │
│  Note: Exact times vary per run via seeded PPO policy noise.        │
└──────────────────────────────────────────────────────────────────────┘
```

**Benefits**: The PPO reward function creates a natural speed-accuracy
tradeoff: faster stations may sacrifice injection precision, while
accuracy-focused stations take more time. Different random seeds during
policy training produce genuinely distinct behavior profiles, making each
competition run a unique race between four plausible strategies.

### Diagram 3: Multi-Station 3D Layout and Technology Stack

```
┌──────────────────────────────────────────────────────────────────────┐
│      MULTI-STATION 3D LAYOUT & TECHNOLOGY STACK (v0.3.0)             │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌────────────────── HOSPITAL ROOM (14m × 14m) ────────────────-┐  │
│  │                                                               │  │
│  │  ┌── Station A ──────┐    ┌── Station B ──────┐              │  │
│  │  │ [Doc]  [Pat]  [Nrs]│    │ [Doc]  [Pat]  [Nrs]│             │  │
│  │  │  (L)   chair   (R) │    │  (L)   chair   (R) │             │  │
│  │  │  tab   IV+mon  syr │    │  tab   IV+mon  syr │             │  │
│  │  │       [●target]     │    │       [●target]     │             │  │
│  │  └────────────────────┘    └────────────────────┘             │  │
│  │        5.0m spacing             5.0m spacing                  │  │
│  │  ┌── Station C ──────┐    ┌── Station D ──────┐              │  │
│  │  │ [Doc]  [Pat]  [Nrs]│    │ [Doc]  [Pat]  [Nrs]│             │  │
│  │  │  (L)   chair   (R) │    │  (L)   chair   (R) │             │  │
│  │  │  tab   IV+mon  syr │    │  tab   IV+mon  syr │             │  │
│  │  │       [●target]     │    │       [●target]     │             │  │
│  │  └────────────────────┘    └────────────────────┘             │  │
│  │        5.0m row spacing                                       │  │
│  │  Legend: Doc=Doctor(white) Pat=Patient(green) Nrs=Nurse(blue) │  │
│  │          ●=injection target tab=tablet syr=syringe            │  │
│  └───────────────────────────────────────────────────────────────┘  │
│                                                                      │
│  LAYER 1: PHYSICS ENGINE                                             │
│  ┌────────────────────────────────────────────────────────────┐     │
│  │  MuJoCo (Multi-Joint dynamics with Contact)                │     │
│  │  ├── 4-station MJCF XML scene (competition_scene.xml)      │     │
│  │  ├── 48 joint actuators (12 per station × 4)               │     │
│  │  ├── 8 contact sensors (needle_tip + target per station)   │     │
│  │  ├── Injection target marker on each patient's deltoid     │     │
│  │  └── 0.002s timestep, position-controlled actuators        │     │
│  └────────────────────────────────────────────────────────────┘     │
│                          │                                           │
│  LAYER 2: PPO POLICY LAYER                                           │
│  ┌────────────────────────────────────────────────────────────┐     │
│  │  Proximal Policy Optimization (PPO)                        │     │
│  │  ├── MLP 64×64 with tanh activation (per station)          │     │
│  │  ├── 4 seeds: 42, 137, 256, 512 → 4 distinct policies     │     │
│  │  ├── Reward: speed (-0.3) + accuracy (0.5) + smooth (0.2)  │     │
│  │  ├── Observation: phase, joints, needle pos, target, time   │     │
│  │  └── Action: shoulder/elbow/wrist deltas, approach velocity │     │
│  └────────────────────────────────────────────────────────────┘     │
│                          │                                           │
│  LAYER 3: VISUALIZATION                                              │
│  ┌────────────────────────────────────────────────────────────┐     │
│  │  Three.js r169 Competition Viewer (docs/v2/index.html)     │     │
│  │  ├── 12 articulated G1 humanoid robots (3 per station)     │     │
│  │  ├── WebGL PBR rendering, PCF soft shadows                 │     │
│  │  ├── Closable scoreboard + closable phase timeline         │     │
│  │  ├── Final results overlay (1st/2nd/3rd/4th + times + acc) │     │
│  │  ├── Cross-viewer navigation banner                        │     │
│  │  └── Responsive: iPhone, Android, tablet, desktop          │     │
│  └────────────────────────────────────────────────────────────┘     │
│                          │                                           │
│  LAYER 4: DEPLOYMENT & TESTING                                       │
│  ┌────────────────────────────────────────────────────────────┐     │
│  │  GitHub Pages + CI Pipeline                                │     │
│  │  ├── /docs/index.html → v0.1.x single station             │     │
│  │  ├── /docs/v2/index.html → v0.3.0 competition             │     │
│  │  ├── ruff lint + format (Python 3.10/3.11/3.12)            │     │
│  │  ├── pytest (113 tests: phases, interp, competition,       │     │
│  │  │   export boundaries)                                    │     │
│  │  └── pre-commit hooks for local development                │     │
│  └────────────────────────────────────────────────────────────┘     │
│                                                                      │
│  OPEN-SOURCE STACK (all free, no wandb)                              │
│  ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐           │
│  │MuJoCo  │ │Three.js│ │GitHub  │ │Python  │ │ Ruff   │           │
│  │Apache  │ │  MIT   │ │Actions │ │ PSF    │ │  MIT   │           │
│  │  2.0   │ │        │ │  Free  │ │        │ │        │           │
│  └────────┘ └────────┘ └────────┘ └────────┘ └────────┘           │
└──────────────────────────────────────────────────────────────────────┘
```

## Advances Over mjlab and v0.1.x

| Aspect | mjlab | v0.1.x | v0.3.0 (This Release) |
|---|---|---|---|
| Domain | General RL locomotion | Clinical injection | **Clinical competition** |
| Stations | Single agent | Single station | **4 simultaneous stations** |
| RL Policy | IsaacLab API | Scripted phases | **PPO with seeded training** |
| Roles | Single agent | Doctor + Nurse + Patient | **Doctor(review) + Nurse(inject) + Patient** |
| Measurement | Velocity tracking | Needle distance | **Time + accuracy + rank** |
| UI Panels | N/A | Always visible | **Closable (user preference)** |
| Results | N/A | Single metric | **Final overlay (1st-4th)** |
| Device Support | NVIDIA GPU required | Any browser | **Any browser (mobile-optimized)** |

## Project Structure

```
robot-competition-clinical/
├── .github/workflows/ci.yml           # Lint/format CI for Python 3.10-3.12
├── .pre-commit-config.yaml            # Local ruff hooks
├── docs/
│   ├── index.html                      # v0.1.x Three.js viewer (GitHub Pages)
│   ├── v2/
│   │   └── index.html                  # v0.3.0 Competition viewer (GitHub Pages)
│   └── diagrams/
│       ├── v1_architecture.md          # Archived v0.1.x text diagrams
│       └── v2_architecture.md          # Archived v0.2.0 text diagrams
├── simulation/                         # v0.1.x single-station simulation
│   ├── __init__.py
│   ├── constants.py                    # Shared phase timings + TypedDicts
│   ├── models/
│   │   └── clinical_scene.xml          # MuJoCo MJCF (single station)
│   ├── run_simulation.py               # MuJoCo simulation runner
│   └── export_animation.py             # Animation export to JSON
├── simulation_v2/                      # v0.2+ competition simulation
│   ├── __init__.py
│   ├── constants.py                    # Competition constants + PpoConfig TypedDict
│   ├── ppo_policy.py                   # PPO policy simulation
│   ├── run_competition.py              # 4-station competition runner
│   ├── export_competition.py           # Competition animation export
│   └── models/
│       └── competition_scene.xml       # MuJoCo MJCF (4 stations)
├── tests/
│   ├── __init__.py
│   ├── test_phases.py                  # Phase transition tests
│   ├── test_interpolation.py           # Interpolation + FPS tests
│   ├── test_competition.py             # Competition metric tests
│   └── test_exports.py                 # Export payload boundary tests
├── peer-review/
│   ├── v0.1.1-senior-peer-review.md   # Peer review (14 recommendations)
│   ├── v0.2.1-senior-peer-review.md   # Peer review (10 recommendations)
│   └── v0.3.0-implementation-report.md # Implementation report for v0.3.0
├── .gitignore
├── LICENSE                             # Apache License 2.0
├── README.md                           # This file
├── changelog.md                        # Version history
├── releases.md                         # Release notes
├── prompts.md                          # Build prompts (v0.1.0 — v0.3.0)
└── pyproject.toml                      # Project config + ruff + pytest
```

## Running the Python Simulation (Optional)

The Python backend is optional — the web viewers work independently.

```bash
# Install dependencies
pip install mujoco numpy

# --- v0.3.0 Competition ---
# Run the 4-station competition
python -m simulation_v2.run_competition

# Export competition data for the web viewer
python -m simulation_v2.export_competition --output docs/v2/competition_data.json

# --- v0.1.x Single Station ---
# Run single-station simulation
python -m simulation.run_simulation --export output/animation.json

# Export web animation data
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
