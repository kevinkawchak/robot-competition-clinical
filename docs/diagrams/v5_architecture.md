# v0.5.0 Architecture Diagrams (Archived)

These diagrams document the v0.5.0 architecture. For current architecture, see the README.

## v0.5.0 System Architecture

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
+----------------------------------------------------------------------+
```

## v0.5.0 3D Layout

```
+---------- HOSPITAL ROOM (16m x 16m, NO CEILING) --------------+
|                    (open top — see through)                    |
|  +-- Station A --------+    +-- Station B --------+           |
|  | [Nrs]  [Pat]  [Doc] |    | [Nrs]  [Pat]  [Doc] |           |
|  |  (L)   chair   (R)  |    |  (L)   chair   (R)  |           |
|  |  tab   IV+mon  syr  |    |  tab   IV+mon  syr  |           |
|  +----------------------+    +----------------------+           |
|        5.5m spacing               5.5m spacing                 |
|  +-- Station C --------+    +-- Station D --------+           |
|  | [Nrs]  [Pat]  [Doc] |    | [Nrs]  [Pat]  [Doc] |           |
|  |  (L)   chair   (R)  |    |  (L)   chair   (R)  |           |
|  |  tab   IV+mon  syr  |    |  tab   IV+mon  syr  |           |
|  +----------------------+    +----------------------+           |
|                                                                |
|  Doc=Doctor(white,R,syringe) Pat=Patient(green,robot)          |
|  Nrs=Nurse(blue,L,tablet)                                      |
+----------------------------------------------------------------+
```

## Key Differences (v0.5.0 → v0.6.0)

- v0.5.0 used basic CapsuleGeometry robot models for all participants
- v0.6.0 upgraded to realistic Unitree G1 robot models (unitreerobotics) for doctor/nurse
- v0.6.0 replaced robot patient with realistic human patient model
- v0.6.0 fixed patient orientation, arm placement, and injection target position
