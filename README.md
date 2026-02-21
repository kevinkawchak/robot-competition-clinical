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

**Step 2:** Open the generated URL on any device (desktop, iOS, Android):

| Simulation | URL | Description |
|---|---|---|
| **v0.2.0 Competition** | `https://<user>.github.io/robot-competition-clinical/v2/` | 4-station PPO competition |
| **v0.1.x Single Station** | `https://<user>.github.io/robot-competition-clinical/` | Original single-station injection |

Press **Play** to start the competition and watch all 4 stations race.

## What This Simulates (v0.2.0)

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
| Doctor | Left of patient | White coat, red cross | Tablet | Reviews symptoms/toxicities |
| Patient | Center (seated) | Green gown | Exam chair | Receives injection (right arm) |
| Nurse | Right of patient | Blue coat, badge | Syringe | Performs deltoid injection |

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

### Measurement

- **Time**: Elapsed simulation seconds from start to nurse withdrawal completion
- **Accuracy**: Euclidean distance (meters) between needle tip and injection target site
- **Accuracy Score**: `1.0 / (1.0 + distance * 100.0)` — higher is better
- **PPO Reward**: Weighted sum of time penalty, accuracy reward, and smoothness reward

## Features

- **4-Station Competition**: Simultaneous independent simulation across all stations
- **PPO RL Policies**: Distinct behavior from seeded policy training
- **Real-Time Scoreboard**: Doctor time, nurse time, total time, accuracy, rank
- **Cross-Device 3D Viewer**: Desktop, iOS, Android via Three.js
- **Zero Installation**: View directly from GitHub Pages
- **MuJoCo Physics**: Full MJCF scene models with articulated humanoids
- **Interactive Controls**: Play/pause, reset, progress scrubbing, station camera focus
- **File Upload**: Upload custom JSON/XML for future configurations
- **Mobile-Friendly**: Responsive layout with collapsible scoreboard
- **Dual Viewers**: Separate GitHub Pages for v1 and v2 simulations
- **Open & Free**: All dependencies open-source (no wandb)

## Uploading Custom Simulations

To upload custom data for future simulations:

1. **v0.2.0 Competition**: Generate a `competition_data.json` file using
   `python -m simulation_v2.export_competition --output competition_data.json`
   and upload it via the **Upload** button in the `/v2/` viewer.

2. **v0.1.x Single Station**: Generate an `animation_data.json` file using
   `python -m simulation.export_animation --output animation_data.json`
   and upload it via the **Upload** button in the root viewer.

The viewer will parse the JSON structure and apply it to the simulation.

## Architecture Diagrams

### Diagram 1: Multi-Station Competition Architecture

```
┌──────────────────────────────────────────────────────────────────────┐
│          CLINICAL ROBOT COMPETITION — SYSTEM ARCHITECTURE            │
│                    4-Station PPO Simulation                           │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌──────────────────────┐        ┌───────────────────────────────┐  │
│  │  MuJoCo Backend      │        │   Three.js Competition Viewer │  │
│  │  (Python)            │        │   (HTML/JS - docs/v2/)        │  │
│  │                      │        │                               │  │
│  │ ┌──────────────────┐ │  JSON  │ ┌───────────────────────────┐│  │
│  │ │ competition_scene│ │ ─────► │ │ 4-Station 3D Renderer    ││  │
│  │ │ .xml (4 stations)│ │ export │ │ - 2x2 Grid Layout        ││  │
│  │ └──────────────────┘ │        │ │ - 12 G1 Humanoid Models  ││  │
│  │        │             │        │ │ - 4x Medical Equipment   ││  │
│  │        ▼             │        │ └───────────────────────────┘│  │
│  │ ┌──────────────────┐ │        │          │                    │  │
│  │ │ ppo_policy.py    │ │        │          ▼                    │  │
│  │ │ - PPO MLP 64x64  │ │        │ ┌───────────────────────────┐│  │
│  │ │ - 4 seed configs │ │        │ │ Per-Station Animation    ││  │
│  │ │ - Reward function│ │        │ │ - Doctor review (4 phase) ││  │
│  │ └──────────────────┘ │        │ │ - Nurse inject (6 phase)  ││  │
│  │        │             │        │ │ - Independent timing      ││  │
│  │        ▼             │        │ └───────────────────────────┘│  │
│  │ ┌──────────────────┐ │        │          │                    │  │
│  │ │ run_competition  │ │        │          ▼                    │  │
│  │ │ .py              │ │        │ ┌───────────────────────────┐│  │
│  │ │ - 4 stations     │ │        │ │ Competition UI           ││  │
│  │ │ - Metrics/rank   │ │        │ │ - Scoreboard (4 stations)││  │
│  │ └──────────────────┘ │        │ │ - Station selector A-D   ││  │
│  │        │             │        │ │ - Play/Pause/Reset       ││  │
│  │        ▼             │        │ │ - Upload + Info          ││  │
│  │ ┌──────────────────┐ │        │ └───────────────────────────┘│  │
│  │ │ export_competitn │ │        │          │                    │  │
│  │ │ .py              │ │        │          ▼                    │  │
│  │ │ - Station frames │ │        │ ┌───────────────────────────┐│  │
│  │ │ - JSON output    │ │        │ │ Device Targets           ││  │
│  │ └──────────────────┘ │        │ │ ✓ Desktop (mouse+kb)     ││  │
│  │                      │        │ │ ✓ iOS (touch+pinch)      ││  │
│  └──────────────────────┘        │ │ ✓ Android (touch+pinch)  ││  │
│                                  │ └───────────────────────────┘│  │
│  ┌──────────────────────┐        └───────────────────────────────┘  │
│  │   CI/CD + Testing    │                                           │
│  │ - ruff lint/format   │     ┌───────────────────────────────┐    │
│  │ - pytest smoke tests │     │  v0.1.x Single-Station Viewer │    │
│  │ - Python 3.10-3.12   │     │  (docs/index.html — separate) │    │
│  │ - pre-commit hooks   │     └───────────────────────────────┘    │
│  └──────────────────────┘                                           │
│                                                                      │
│  Attribution: Inspired by mjlab (mujocolab/mjlab)                   │
└──────────────────────────────────────────────────────────────────────┘
```

**Benefits**: Dual-viewer architecture provides both single-station and
competition experiences via separate GitHub Pages URLs. The PPO policy layer
enables distinct per-station behaviors from a single codebase. JSON export
bridges MuJoCo physics with zero-install web viewing on any device.

### Diagram 2: PPO Competition Workflow

```
┌──────────────────────────────────────────────────────────────────────┐
│              PPO COMPETITION WORKFLOW — 4-STATION RACE               │
│              Doctor Review → Nurse Injection → Ranking               │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌─── STATION A (seed=42) ──────────────────────────────────────┐   │
│  │ DOCTOR REVIEW            │ NURSE INJECTION                    │   │
│  │ [recv][review][assess][ok]│[prep][approach][pos][inject][hold][wd]│
│  │ ◄── 5.5s base ──────────►│◄── 8.5s base ────────────────────►│   │
│  └──────────────────────────────────────────────────────────────-┘   │
│  ┌─── STATION B (seed=137, faster) ────────────────────────────-┐   │
│  │ DOCTOR REVIEW          │ NURSE INJECTION                      │   │
│  │ [recv][review][asses][ok]│[prep][appr][pos][inject][hold][wd] │   │
│  │ ◄── ~4.8s ────────────►│◄── ~7.5s ──────────────────────────►│   │
│  └──────────────────────────────────────────────────────────────-┘   │
│  ┌─── STATION C (seed=256, most accurate) ─────────────────────-┐   │
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
│  ┌────────────────────── PPO REWARD FUNCTION ──────────────────-┐   │
│  │                                                               │   │
│  │  R = -0.3 × time  +  0.5 / (1 + dist)  +  0.2 / (1 + jerk) │   │
│  │       ▲                   ▲                    ▲              │   │
│  │       │                   │                    │              │   │
│  │   Speed penalty     Accuracy reward     Smoothness reward    │   │
│  │   (lower time =     (closer needle =    (less jerk =        │   │
│  │    higher reward)    higher reward)      higher reward)      │   │
│  │                                                               │   │
│  │  Policy: MLP 64×64, tanh | γ=0.99 | clip=0.2 | lr=3e-4     │   │
│  └───────────────────────────────────────────────────────────────┘   │
│                                                                      │
│  ┌────────────────── COMPETITION SCOREBOARD ───────────────────-┐   │
│  │  Rank │ Station │ Dr Time │ Nurse Time │ Total │ Accuracy   │   │
│  │  ─────┼─────────┼─────────┼────────────┼───────┼──────────  │   │
│  │   #1  │    B    │  4.84s  │   7.48s    │ 12.3s │  0.643     │   │
│  │   #2  │    D    │  5.22s  │   8.05s    │ 13.3s │  0.435     │   │
│  │   #3  │    A    │  5.50s  │   8.50s    │ 14.0s │  0.500     │   │
│  │   #4  │    C    │  5.94s  │   9.18s    │ 15.1s │  0.625     │   │
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
│      MULTI-STATION 3D LAYOUT & TECHNOLOGY STACK                      │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌────────────────── HOSPITAL ROOM (12m × 12m) ────────────────-┐  │
│  │                                                               │  │
│  │  ┌── Station A ──────┐    ┌── Station B ──────┐              │  │
│  │  │ [Doc]  [Pat]  [Nrs]│    │ [Doc]  [Pat]  [Nrs]│             │  │
│  │  │  (L)   chair   (R) │    │  (L)   chair   (R) │             │  │
│  │  │  tab   IV+mon  syr │    │  tab   IV+mon  syr │             │  │
│  │  └────────────────────┘    └────────────────────┘             │  │
│  │        4.5m spacing             4.5m spacing                  │  │
│  │  ┌── Station C ──────┐    ┌── Station D ──────┐              │  │
│  │  │ [Doc]  [Pat]  [Nrs]│    │ [Doc]  [Pat]  [Nrs]│             │  │
│  │  │  (L)   chair   (R) │    │  (L)   chair   (R) │             │  │
│  │  │  tab   IV+mon  syr │    │  tab   IV+mon  syr │             │  │
│  │  └────────────────────┘    └────────────────────┘             │  │
│  │        4.0m row spacing                                       │  │
│  │  Legend: Doc=Doctor(white) Pat=Patient(green) Nrs=Nurse(blue) │  │
│  │          tab=tablet syr=syringe IV=IV stand mon=vitals monitor│  │
│  └───────────────────────────────────────────────────────────────┘  │
│                                                                      │
│  LAYER 1: PHYSICS ENGINE                                             │
│  ┌────────────────────────────────────────────────────────────┐     │
│  │  MuJoCo (Multi-Joint dynamics with Contact)                │     │
│  │  ├── 4-station MJCF XML scene (competition_scene.xml)      │     │
│  │  ├── 48 joint actuators (12 per station × 4)               │     │
│  │  ├── 8 contact sensors (needle_tip + target per station)   │     │
│  │  ├── Rigid body dynamics, 9.81 m/s² gravity                │     │
│  │  └── 0.002s timestep, position-controlled actuators        │     │
│  │  Benefit: Research-grade physics across all 4 stations      │     │
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
│  │  Benefit: Principled RL produces realistic behavior variety │     │
│  └────────────────────────────────────────────────────────────┘     │
│                          │                                           │
│  LAYER 3: VISUALIZATION                                              │
│  ┌────────────────────────────────────────────────────────────┐     │
│  │  Three.js r169 Competition Viewer (docs/v2/index.html)     │     │
│  │  ├── 12 articulated G1 humanoid robots (3 per station)     │     │
│  │  ├── WebGL PBR rendering, PCF soft shadows                 │     │
│  │  ├── Station-focus camera with A/B/C/D selector buttons    │     │
│  │  ├── Competition scoreboard with live metrics              │     │
│  │  └── Responsive layout: desktop, iOS, Android              │     │
│  │  Benefit: Simultaneous 4-station visualization, any device  │     │
│  └────────────────────────────────────────────────────────────┘     │
│                          │                                           │
│  LAYER 4: DEPLOYMENT & TESTING                                       │
│  ┌────────────────────────────────────────────────────────────┐     │
│  │  GitHub Pages + CI Pipeline                                │     │
│  │  ├── /docs/index.html → v0.1.x single station             │     │
│  │  ├── /docs/v2/index.html → v0.2.0 competition             │     │
│  │  ├── ruff lint + format (Python 3.10/3.11/3.12)            │     │
│  │  ├── pytest unit tests (phases, interpolation, competition)│     │
│  │  └── pre-commit hooks for local development                │     │
│  │  Benefit: Dual viewers, automated quality checks            │     │
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

**Benefits**: The 2x2 grid layout maximizes visual comparison across stations
while maintaining proper 3D spacing for camera orbiting. Four technology
layers cleanly separate physics, RL policy, visualization, and deployment.
The PPO policy layer is the key differentiator from v0.1.x, enabling
autonomous behavior variation from a shared codebase.

## Advances Over mjlab and v0.1.x

| Aspect | mjlab | v0.1.x | v0.2.0 (This Release) |
|---|---|---|---|
| Domain | General RL locomotion | Clinical injection | **Clinical competition** |
| Stations | Single agent | Single station | **4 simultaneous stations** |
| RL Policy | IsaacLab API | Scripted phases | **PPO with seeded training** |
| Roles | Single agent | Doctor + Nurse + Patient | **Doctor(review) + Nurse(inject) + Patient** |
| Measurement | Velocity tracking | Needle distance | **Time + accuracy + rank** |
| Device Support | NVIDIA GPU required | Any browser | **Any browser (mobile-friendly)** |

## Project Structure

```
robot-competition-clinical/
├── .github/workflows/ci.yml           # Lint/format/test CI for Python 3.10-3.12
├── .pre-commit-config.yaml            # Local ruff hooks
├── docs/
│   ├── index.html                      # v0.1.x Three.js viewer (GitHub Pages)
│   ├── v2/
│   │   └── index.html                  # v0.2.0 Competition viewer (GitHub Pages)
│   └── diagrams/
│       └── v1_architecture.md          # Archived v0.1.x text diagrams
├── simulation/                         # v0.1.x single-station simulation
│   ├── __init__.py
│   ├── constants.py                    # Shared phase timings + TypedDicts
│   ├── models/
│   │   └── clinical_scene.xml          # MuJoCo MJCF (single station)
│   ├── run_simulation.py               # MuJoCo simulation runner
│   └── export_animation.py             # Animation export to JSON
├── simulation_v2/                      # v0.2.0 competition simulation
│   ├── __init__.py
│   ├── constants.py                    # Competition constants + station configs
│   ├── ppo_policy.py                   # PPO policy simulation
│   ├── run_competition.py              # 4-station competition runner
│   ├── export_competition.py           # Competition animation export
│   └── models/
│       └── competition_scene.xml       # MuJoCo MJCF (4 stations)
├── tests/
│   ├── __init__.py
│   ├── test_phases.py                  # Phase transition tests
│   ├── test_interpolation.py           # Interpolation + FPS tests
│   └── test_competition.py             # Competition metric tests
├── peer-review/
│   └── v0.1.1-senior-peer-review.md   # Peer review with 14 recommendations
├── .gitignore
├── LICENSE                             # Apache License 2.0
├── README.md                           # This file
├── changelog.md                        # Version history
├── releases.md                         # Release notes
├── prompts.md                          # Build prompts (v0.1.0 + v0.2.0)
└── pyproject.toml                      # Project config + ruff + pytest
```

## Running the Python Simulation (Optional)

The Python backend is optional — the web viewers work independently.

```bash
# Install dependencies
pip install mujoco numpy

# --- v0.2.0 Competition ---
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

## Running Tests

```bash
pip install pytest
pytest tests/
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
