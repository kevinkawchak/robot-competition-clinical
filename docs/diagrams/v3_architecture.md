# v0.3.0 Architecture Diagrams (Archived)

These diagrams were the architecture documentation for the v0.3.0 4-station
clinical competition simulation with closable UI panels. They have been
preserved here for reference. The main README now contains updated diagrams
for v0.4.0.

## Diagram 1: Multi-Station Competition Architecture (v0.3.0)

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

## Diagram 2: PPO Competition Workflow (v0.3.0)

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

## Diagram 3: Multi-Station 3D Layout and Technology Stack (v0.3.0)

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
│  Dark theme: #0f0f1e base, #00d4ff accent                           │
│  Three.js r169, WebGL PBR, PCF soft shadows                         │
│  Responsive: 3 breakpoints (default, 768px, 420px)                  │
│                                                                      │
│  OPEN-SOURCE STACK (all free, no wandb)                              │
│  ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐           │
│  │MuJoCo  │ │Three.js│ │GitHub  │ │Python  │ │ Ruff   │           │
│  │Apache  │ │  MIT   │ │Actions │ │ PSF    │ │  MIT   │           │
│  │  2.0   │ │        │ │  Free  │ │        │ │        │           │
│  └────────┘ └────────┘ └────────┘ └────────┘ └────────┘           │
└──────────────────────────────────────────────────────────────────────┘
```
