# v0.4.0 Architecture Diagrams (Archived)

Archived from README.md when v0.5.0 was released.

## Diagram 1: Multi-Station Competition Architecture (v0.4.0)

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

## Diagram 2: PPO Competition Workflow (v0.4.0)

```
+----------------------------------------------------------------------+
|              PPO COMPETITION WORKFLOW - 4-STATION RACE                |
|     v0.4.0: Doctor Review (4 phases) -> Nurse Injection (6 phases)   |
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
+----------------------------------------------------------------------+
```

## Diagram 3: Full-Detail 3D Layout (v0.4.0)

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
|  |  +--------------------+    +--------------------+             |   |
|  |        5.5m spacing             5.5m spacing                  |   |
|  |  +-- Station C ------+    +-- Station D ------+              |   |
|  |  | [Doc]  [Pat]  [Nrs]|    | [Doc]  [Pat]  [Nrs]|             |   |
|  |  |  (L)   chair   (R) |    |  (L)   chair   (R) |             |   |
|  |  |  tab   IV+mon  syr |    |  tab   IV+mon  syr |             |   |
|  |  +--------------------+    +--------------------+             |   |
|  +---------------------------------------------------------------+   |
|                                                                      |
|  v0.4.0 Layout: Doctor LEFT (tablet), Nurse RIGHT (syringe)         |
|  v0.4.0 Phases: 4 doctor review + 6 nurse injection = 10 total      |
+----------------------------------------------------------------------+
```
