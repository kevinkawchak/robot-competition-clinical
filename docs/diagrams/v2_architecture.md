# v0.2.0 Architecture Diagrams (Archived)

These diagrams were the architecture documentation for the v0.2.0 4-station
clinical competition simulation. They have been preserved here for reference.
The main README now contains updated diagrams for v0.3.0.

## Diagram 1: Multi-Station Competition Architecture (v0.2.0)

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
│  │ └──────────────────┘ │        │ │ - Desktop (mouse+kb)     ││  │
│  │                      │        │ │ - iOS (touch+pinch)      ││  │
│  └──────────────────────┘        │ │ - Android (touch+pinch)  ││  │
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

## Diagram 2: PPO Competition Workflow (v0.2.0)

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
│  │  R = -0.3 × time  +  0.5 / (1 + dist)  +  0.2 / (1 + jerk) │   │
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
└──────────────────────────────────────────────────────────────────────┘
```

## Diagram 3: Multi-Station 3D Layout and Technology Stack (v0.2.0)

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
│  └───────────────────────────────────────────────────────────────┘  │
│                                                                      │
│  OPEN-SOURCE STACK (all free, no wandb)                              │
│  ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐           │
│  │MuJoCo  │ │Three.js│ │GitHub  │ │Python  │ │ Ruff   │           │
│  │Apache  │ │  MIT   │ │Actions │ │ PSF    │ │  MIT   │           │
│  │  2.0   │ │        │ │  Free  │ │        │ │        │           │
│  └────────┘ └────────┘ └────────┘ └────────┘ └────────┘           │
└──────────────────────────────────────────────────────────────────────┘
```
