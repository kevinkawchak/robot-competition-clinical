# Clinical Robot Competition

MuJoCo-based clinical trial simulation with **Unitree G1 humanoid robots**
(from [unitreerobotics](https://www.unitree.com/g1/)) competing across **four simultaneous
stations** in a 2x2 grid. At each station a **doctor G1 robot** (white coat, 43 DOF incl.
Dex3-1 dexterous hands) and a **nurse G1 robot** (scrub-blue coat) execute a complete
**GCP-aligned 12-phase intramuscular injection visit** on a **realistic human trial
participant**, while a **human Clinical Research Associate (CRA)** observes from a sponsor
monitoring desk. All stations are driven by **PPO reinforcement learning** policies with
distinct behavior profiles from different random seeds, and are ranked by a **composite
GCP score** spanning time, needle accuracy, protocol adherence, sterility, dose precision,
and participant comfort.

v1.0.0 is the recommended viewer — a ground-up, state-of-the-art rebuild for clinical trial
experts: high-DOF robots with articulated fingers and gait, an IK tip-correction system that
guarantees frame-accurate needle-to-deltoid contact (eliminating the historical object-overlap
and needle-gap bugs by construction), a photoreal **open-top room (no ceiling)**, live animated
ECG monitors, a central live scoreboard tower, a seeded Grade 1 adverse event with autonomous
response, and a zoom-anywhere camera (0.05 m minimum distance, zoom-to-cursor, double-click
focus on any object in the room).

The objective is to illustrate that having competitions across multiple autonomous robots is
advantageous for making upcoming fully autonomous physical AI oncology trials faster than current
human trials.

Built as the next step beyond [mjlab](https://github.com/mujocolab/mjlab)
(mujocolab/mjlab), extending GPU-accelerated robot simulation into clinical
competition scenarios with universal device accessibility.

## Quick Start (1-2 Steps from GitHub)

**Step 1:** Enable GitHub Pages in your fork:
Settings → Pages → Source: "Deploy from a branch" → Branch: `main`, Folder: `/docs` → Save

> **If every page returns 404:** first check the serving self-test at
> [`/health.txt`](https://kevinkawchak.github.io/robot-competition-clinical/health.txt).
> If `health.txt` also 404s even though the latest **"pages build and deployment"** run
> under the Actions tab is green, the Pages site routing is stuck and must be re-created
> from the browser: Settings → Pages → set Source to **None** → Save → wait one minute →
> set Source back to **Deploy from a branch** (`main`, `/docs`) → Save. If instead
> `health.txt` loads, the site is fine — a missing path now shows this project's own
> [404 page](docs/404.html) with links to every version.

**Step 2:** Open the simulation on any device (desktop, iOS, Android):

| Version | URL | Description |
|---|---|---|
| **v1.0.0 GCP Trial Suite (new)** | [https://kevinkawchak.github.io/robot-competition-clinical/v10/](https://kevinkawchak.github.io/robot-competition-clinical/v10/) | 12-phase GCP visit, 43-DOF robots, IK needle contact, composite scoring, open-top photoreal suite, AE response, human CRA |
| **v0.9.0 Competition** | [https://kevinkawchak.github.io/robot-competition-clinical/v9/](https://kevinkawchak.github.io/robot-competition-clinical/v9/) | v0.6.0 base + patient seating, facial features, close-zoom, no shoulder Z-fight, needle-contact |
| **v0.8.0 Competition** | [https://kevinkawchak.github.io/robot-competition-clinical/v8/](https://kevinkawchak.github.io/robot-competition-clinical/v8/) | SOTA G1 robots, realistic patients, premium dark theme, PBR visuals |
| **v0.7.0 Competition** | [https://kevinkawchak.github.io/robot-competition-clinical/v7/](https://kevinkawchak.github.io/robot-competition-clinical/v7/) | Enhanced visuals: ceiling lights, patient faces, active nurse |
| **v0.6.0 Competition** | [https://kevinkawchak.github.io/robot-competition-clinical/v6/](https://kevinkawchak.github.io/robot-competition-clinical/v6/) | Realistic Unitree G1 robots + human patient |
| **v0.5.0 Competition** | [https://kevinkawchak.github.io/robot-competition-clinical/v5/](https://kevinkawchak.github.io/robot-competition-clinical/v5/) | 4-station PPO competition (light mode, open-top) |
| **v0.1.0 Single Station** | [https://kevinkawchak.github.io/robot-competition-clinical/](https://kevinkawchak.github.io/robot-competition-clinical/) | Original single-station injection (stable) |

Press **Play** to start the competition and watch all 4 stations run the GCP visit. Use the
toggle buttons to open the **GCP Phase Timeline + Live Telemetry** and **GCP Scoreboard**
panels. When all stations finish, the **Final GCP Results** overlay displays the composite
ranking. Scroll/pinch zooms toward the cursor; **double-click (or double-tap) any object** —
a fingertip, the needle, the ECG trace, a poster — to glide the camera to it.

## What This Simulates (v1.0.0)

Four identical stations compete simultaneously to complete a **GCP-aligned 12-phase IM
injection visit** on diverse, realistic human participants (per-station skin tone, hairstyle,
gown color; blinking, breathing, consent nods, armrest grip during injection). The doctor and
nurse are **43-DOF Unitree G1 humanoids** whose articulated fingers actually grip the syringe,
swab, vial, scanner, and tablet; their legs run a gait cycle whenever they walk between the
patient and the supply cart. A runtime **IK tip-correction** servo drives the needle tip onto
the deltoid target every frame — touching the surface at insertion and sitting 6 mm indwelling
during the slow-push dose — with zero interpenetration. One seeded station experiences a
**Grade 1 vasovagal adverse event** during observation (ECG dips to ~49 bpm, patient's head
droops, nurse leans in, observation extends), demonstrating autonomous AE surveillance. A
**human CRA** monitors everything from a sponsor desk with a live EDC laptop, and a central
**4-face scoreboard tower** broadcasts live ranks. The room is open-top (no ceiling) with
daylight + per-station freestanding exam-light booms, procedural floor/wall textures, an
observation window, signage posters, and full per-station equipment.

### v1.0.0 Headline Upgrades

| # | Area | v1.0.0 Upgrade |
|---|---|---|
| 1 | High-DOF robots | 43 DOF per G1: 7-DOF arms, 7-DOF Dex3-1 hands with 2-segment articulated fingers, 3-DOF waist, 2-DOF neck, 6-DOF legs with gait cycle |
| 2 | Physical overlap | Fixed by construction: coat = torso shell (no overlay z-fight), verified prop clearances, patient soles exactly on floor, props flush on surfaces, IK prevents needle interpenetration |
| 3 | Competition realism | 12-phase GCP workflow, composite GCP scoring, seeded Grade 1 AE with response, live ECG/SpO2/NIBP, eSource documentation, human-in-the-loop CRA |
| 4 | Room | Open-top (no ceiling), photoreal textures, observation window + hallway, posters, privacy screens, exam-light booms, supply carts, sharps containers, scoreboard tower |
| 5 | Zoom | minDistance 0.05 m, zoom-to-cursor, fog removed, double-click/double-tap glide-focus on any object, per-station camera presets, keyboard shortcuts |

### 12-Phase GCP Visit Per Station (v1.0.0)

| # | Phase | Actor | Base | What Happens |
|---|-------|-------|------|--------------|
| 1 | Identity verification | Nurse | 1.2s | Wristband scan (two identifiers), scanner LED blinks |
| 2 | eConsent confirmation | Nurse | 1.2s | Tablet raised to participant, participant nods |
| 3 | Baseline vitals | Nurse | 1.4s | ECG/SpO2/NIBP captured on the live monitor |
| 4 | Hand hygiene & gloves | Doctor | 1.2s | Hand rub at the sanitizer |
| 5 | Drug prep & barcode check | Doctor | 2.2s | Walks to cart, draws 0.50 mL from vial (gait + finger grip) |
| 6 | Aseptic site prep | Doctor | 1.6s | Alcohol swab circles the right deltoid (left hand, IK) |
| 7 | Landmark & alignment | Doctor | 1.4s | Needle aligned to target (IK ramps in) |
| 8 | Needle insertion | Doctor | 1.2s | 90° IM — tip meets the deltoid surface exactly |
| 9 | Dose delivery | Doctor | 2.4s | Plunger depresses, fluid empties, 6 mm indwelling |
| 10 | Withdraw & safety | Doctor | 1.0s | Needle out, IK releases |
| 11 | Sharps disposal | Doctor | 1.4s | Syringe dropped into sharps container, LED confirms |
| 12 | Observation & eSource | Nurse | 2.3s | Documentation taps; AE surveillance (extended +2.5s/speed on AE) |

**Total base duration:** 18.5 seconds. PPO jitter and speed profiles produce actual visit
times of ~18.8–19.9 s.

### Station Layout (2x2 Grid)

| Station | Position | Seed | Speed | Patient | Profile |
|---------|----------|------|-------|---------|---------|
| **A** | Front-left | 42 | 1.00x | Light skin, short brown hair, mint gown | Balanced |
| **B** | Front-right | 137 | 0.93x | Deep brown skin, black curly hair, light-blue gown | Speed-focused |
| **C** | Back-left | 256 | 1.07x | Tan skin, long dark hair, lavender gown | Careful (draws the Grade 1 AE) |
| **D** | Back-right | 512 | 0.97x | Pale skin, grey hair, peach gown | Precision-focused |

### Role Assignments (v1.0.0)

| Role | Position | Appearance | Equipment | Action |
|------|----------|------------|-----------|--------|
| Doctor (G1) | Right of patient, walks to cart | Charcoal G1, white coat shell, red cross, glossy visor | Syringe (IK-corrected needle), swab, vial | Hygiene, drug prep, site prep, injection, dose, sharps disposal |
| Nurse (G1) | Left of patient | Charcoal G1, scrub-blue coat shell, gold badge | Tablet (always), wristband scanner | Identity check, eConsent, vitals, observation, eSource documentation |
| Patient (Human) | Infusion recliner, feet on floor | Diverse per station; blinks, breathes, nods, grips armrest | Wristband, live ECG leads | Receives the 0.50 mL IM dose (right deltoid) |
| CRA (Human) | Sponsor monitoring desk | Business casual, ID badge | EDC laptop, monitoring banner | Human-in-the-loop oversight; types, scans the room |

### Composite GCP Scoring (v1.0.0)

`Composite = 0.30×Time + 0.25×Accuracy + 0.20×Protocol + 0.10×Sterility + 0.10×Dose + 0.05×Comfort`

- **Time score**: `100 × (fastest_total / station_total)` over all 12 phases (incl. AE extension)
- **Accuracy score**: `100 − 18 × needle_deviation_mm` (recorded placement deviation)
- **Protocol adherence**: seeded 96–100% (visit-schedule deviations)
- **Sterility index**: seeded 97–100% (aseptic technique)
- **Dose score**: `100 − 4000 × |delivered − 0.500 mL|`
- **Comfort index**: seeded 88–100 (motion-jerk proxy)
- **Ranking**: composite descending, total time ascending as tiebreak
- **AE policy**: the AE station's extended observation costs time; safety response itself is
  never penalized

### PPO Reinforcement Learning Details

All four stations use **Proximal Policy Optimization (PPO)** with:

- **Architecture**: 2-layer MLP (64 hidden units each), tanh activation
- **Observation space**: `[phase_progress, arm_joint_angles, needle_pos, target_pos, elapsed_time]`
- **Action space**: `[shoulder_pitch_delta, elbow_delta, wrist_delta, approach_velocity]`
- **Reward function**: `R = -0.3 * elapsed_time + 0.5 / (1 + needle_dist) + 0.2 / (1 + motion_jerk)`
- **Training**: 500 episodes, gamma=0.99, clip_ratio=0.2, learning_rate=3e-4
- **Key insight**: Same policy architecture + different random seeds produces different learned behaviors

**Same policy, different state**: Each station shares the same MLP architecture and PPO
hyperparameters. The only difference between stations is the random seed used during training
initialization (42, 137, 256, 512). This produces genuinely distinct learned parameters —
different speed/accuracy/protocol trade-offs — from the same reward function.

### Simulation Results (v1.0.0, deterministic from seeds)

| Rank | Station | Composite | Total Time | Needle Dev | Protocol | Sterility | Dose | Notes |
|------|---------|-----------|-----------|------------|----------|-----------|------|-------|
| #1 | **D** | **94.8** | 18.84s | 0.76mm | 98.6% | 98.8% | 0.497mL | Precision wins |
| #2 | A | 89.8 | 18.89s | 2.04mm | 97.2% | 97.6% | 0.500mL | Perfect dose |
| #3 | B | 86.0 | 19.46s | 2.41mm | 97.1% | 97.8% | 0.503mL | |
| #4 | C | 84.7 | 19.82s | 2.32mm | 97.2% | 97.3% | 0.495mL | Grade 1 vasovagal AE, resolved |

**Winner: Station D** — near-fastest visit with sub-millimeter needle placement,
demonstrating that the composite GCP score rewards precision + speed together rather than
raw speed alone (Station B, the raw-time winner of v0.x, places #3 under GCP scoring).

## Features

- **12-Phase GCP Workflow** (v1.0.0): identity → eConsent → vitals → hygiene → drug prep →
  site prep → alignment → insertion → dose → withdraw → sharps → observation/eSource
- **43-DOF G1 Robots** (v1.0.0): articulated Dex3-1 fingers that grip, 3-DOF waist, 2-DOF
  neck, wrist supination, leg gait during walking
- **IK Needle Contact** (v1.0.0): tip servo-driven onto the deltoid target every frame —
  surface at insertion, 6 mm indwelling at dose, zero interpenetration
- **Overlap-Free Scene** (v1.0.0): coat-as-shell torsos, verified prop clearances, flush
  prop seating, patient soles exactly on the floor
- **Open-Top Photoreal Room** (v1.0.0): no ceiling, procedural textures, IBL + ACES,
  observation window, posters, privacy screens, exam-light booms
- **Live Clinical Displays** (v1.0.0): animated ECG/SpO2/NIBP per station, central 4-face
  scoreboard tower, EDC laptop at the CRA desk
- **Seeded Grade 1 AE** (v1.0.0): vasovagal episode at Station C with ECG dip, patient
  response, nurse response, extended observation, scoreboard flag
- **Human-in-the-Loop CRA** (v1.0.0): sponsor monitoring desk with a realistic human
- **Diverse Realistic Patients** (v1.0.0): four skin tones/hairstyles/gowns; blinking,
  breathing, nodding, gripping
- **Composite GCP Scoreboard**: time, needle deviation, protocol, sterility, dose, comfort,
  live status, AE flags — closable panel
- **Live Telemetry Panel**: DOF count, live needle→target mm, dose delivered, heart rate,
  eSource latency
- **Zoom-Anywhere Camera**: 0.05 m min distance, zoom-to-cursor, double-click/double-tap
  focus, per-station presets, keyboard shortcuts (Space, R, 0–4)
- **4-Station Competition**: simultaneous independent PPO-seeded stations
- **Final GCP Results Overlay**: composite ranking with times and deviations
- **Metrics Reset**: full deterministic state reset between runs
- **File Upload**: custom JSON configs for station seeds/speeds
- **Cross-Device 3D Viewer**: desktop, iOS, Android via Three.js — zero installation
- **MuJoCo Physics Backend**: MJCF scene models with articulated humanoids (optional)
- **7-Version Nav Banner**: v0.1.0 | v0.5.0 | v0.6.0 | v0.7.0 | v0.8.0 | v0.9.0 | v1.0.0 (new)
- **Open & Free**: all dependencies open-source (no wandb)

## Architecture Diagrams

### Diagram 1: Multi-Station Competition Architecture (v1.0.0)

```
+----------------------------------------------------------------------+
|        CLINICAL ROBOT COMPETITION - SYSTEM ARCHITECTURE v1.0.0       |
|     GCP Trial Suite: 12-phase visit, 43-DOF G1s, composite score     |
+----------------------------------------------------------------------+
|                                                                      |
|  +----------------------+        +-------------------------------+   |
|  |  MuJoCo Backend      |        |   Three.js GCP Trial Suite    |   |
|  |  (Python)            |        |   (HTML/JS - docs/v10/)       |   |
|  |                      |        |                               |   |
|  | +------------------+ |  JSON  | +---------------------------+ |   |
|  | | competition_scene| | -----> | | Open-Top Photoreal Room   | |   |
|  | | .xml (4 stations)| | export | | - 18m x 18m, no ceiling   | |   |
|  | +------------------+ |        | | - 8 G1 robots (43 DOF)    | |   |
|  |        |             |        | | - 4 diverse patients      | |   |
|  |        v             |        | | - human CRA + EDC desk    | |   |
|  | +------------------+ |        | | - live ECG monitors       | |   |
|  | | ppo_policy.py    | |        | | - scoreboard tower        | |   |
|  | | - PPO MLP 64x64  | |        | +---------------------------+ |   |
|  | | - 4 seed configs | |        |          |                    |   |
|  | | - Reward function| |        |          v                    |   |
|  | +------------------+ |        | +---------------------------+ |   |
|  |        |             |        | | 12-Phase GCP Animation    | |   |
|  |        v             |        | | - keyframed pose system   | |   |
|  | +------------------+ |        | | - IK tip correction       | |   |
|  | | run_competition  | |        | | - gait while walking      | |   |
|  | | .py              | |        | | - finger grip/release     | |   |
|  | | - 4 stations     | |        | | - seeded Grade 1 AE       | |   |
|  | | - Metrics/rank   | |        | +---------------------------+ |   |
|  | +------------------+ |        |          |                    |   |
|  |        |             |        |          v                    |   |
|  |        v             |        | +---------------------------+ |   |
|  | +------------------+ |        | | Composite GCP Scoring     | |   |
|  | | export_competitn | |        | | - time/acc/protocol       | |   |
|  | | .py              | |        | | - sterility/dose/comfort  | |   |
|  | | - Station frames | |        | | - live telemetry panel    | |   |
|  | | - JSON output    | |        | | - final results overlay   | |   |
|  | | - Schema v1.0.0  | |        | | - 7-version nav banner    | |   |
|  | +------------------+ |        | +---------------------------+ |   |
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
|  G1 Robots: Unitree Robotics (unitreerobotics)                      |
+----------------------------------------------------------------------+
```

### Diagram 2: GCP Competition Workflow (v1.0.0)

```
+----------------------------------------------------------------------+
|            GCP COMPETITION WORKFLOW - 4-STATION VISIT RACE           |
|   v1.0.0: 12-phase GCP visit, composite scoring, seeded Grade 1 AE   |
+----------------------------------------------------------------------+
|                                                                      |
|  N=nurse  D=doctor                                                   |
|  [identity][consent][vitals][hygiene][drugprep][siteprep][position]  |
|     N         N        N       D         D         D        D       |
|  [inject][dose][withdraw][sharps][monitor+eSource]                   |
|     D      D       D        D        N                               |
|                                                                      |
|  STATION A (seed=42,  1.00x): 18.89s  2.04mm  composite 89.8  #2    |
|  STATION B (seed=137, 0.93x): 19.46s  2.41mm  composite 86.0  #3    |
|  STATION C (seed=256, 1.07x): 19.82s  2.32mm  composite 84.7  #4    |
|             ^ Grade 1 vasovagal AE during monitor (+2.5s/speed)      |
|  STATION D (seed=512, 0.97x): 18.84s  0.76mm  composite 94.8  #1    |
|                                                                      |
|  +--------------- COMPOSITE GCP SCORE -----------------------------+ |
|  |                                                                 | |
|  |  0.30*Time + 0.25*Accuracy + 0.20*Protocol                      | |
|  |          + 0.10*Sterility + 0.10*Dose + 0.05*Comfort            | |
|  |                                                                 | |
|  |  PPO: MLP 64x64 tanh | R = -0.3t + 0.5/(1+d) + 0.2/(1+j)        | |
|  |  Same architecture, 4 seeds -> 4 distinct visit profiles        | |
|  +-----------------------------------------------------------------+ |
|                                                                      |
|  +--------------- FINAL GCP RESULTS -------------------------------+ |
|  |   #1  Station D - 94.8 - 18.84s - 0.76mm  (precision wins)      | |
|  |   #2  Station A - 89.8 - 18.89s - 2.04mm                        | |
|  |   #3  Station B - 86.0 - 19.46s - 2.41mm                        | |
|  |   #4  Station C - 84.7 - 19.82s - 2.32mm  (AE Gr.1, resolved)   | |
|  |           [ Close Results ]  <- user manually replays           | |
|  +-----------------------------------------------------------------+ |
+----------------------------------------------------------------------+
```

### Diagram 3: v1.0.0 3D Layout and Technology Stack

```
+----------------------------------------------------------------------+
|     3D LAYOUT & TECHNOLOGY STACK (v1.0.0 - GCP Trial Suite)          |
+----------------------------------------------------------------------+
|                                                                      |
|  +------- OPEN-TOP SUITE (18m x 18m, NO CEILING) -----------------+  |
|  |   obs window--+                                                |  |
|  |  +-- Station A ---------+    +-- Station B ---------+          |  |
|  |  | [G1n] [Pat] [G1d]    |    | [G1n] [Pat] [G1d]    |          |  |
|  |  | scan  ECG   cart+    |    | scan  ECG   cart+    |          |  |
|  |  | tablet IV   sharps   |    | tablet IV   sharps   |          |  |
|  |  | exam-light boom      |    | exam-light boom      |          |  |
|  |  +----------------------+    +----------------------+          |  |
|  |                  [SCOREBOARD TOWER]                            |  |
|  |  +-- Station C ---------+    +-- Station D ---------+          |  |
|  |  | (Grade 1 AE seeded)  |    | (composite winner)   |          |  |
|  |  +----------------------+    +----------------------+          |  |
|  |                                                                |  |
|  |              [CRA MONITORING DESK + EDC laptop]      door->    |  |
|  +----------------------------------------------------------------+  |
|                                                                      |
|  Legend: G1d=Doctor(white coat shell, syringe w/ IK needle, R)       |
|          Pat=Patient(diverse, blinking, soles on floor)              |
|          G1n=Nurse(scrub-blue coat shell, tablet+scanner, L)         |
|                                                                      |
|  LAYER 1: MuJoCo + PPO (Python backend)                              |
|  LAYER 2: Three.js r169 (docs/v10/index.html) + RoomEnvironment IBL  |
|  LAYER 3: GitHub Pages (static hosting)                              |
|                                                                      |
|  OPEN-SOURCE: MuJoCo(Apache2) Three.js(MIT) Python(PSF) Ruff(MIT)    |
|  ROBOTS: Unitree G1 (unitreerobotics) - unitree.com/g1/              |
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
│   │   └── index.html                  # v0.5.0 Competition viewer
│   ├── v6/
│   │   └── index.html                  # v0.6.0 Competition viewer
│   ├── v7/
│   │   └── index.html                  # v0.7.0 Competition viewer
│   ├── v8/
│   │   └── index.html                  # v0.8.0 Competition viewer
│   ├── v9/
│   │   └── index.html                  # v0.9.0 Competition viewer
│   ├── v10/
│   │   └── index.html                  # v1.0.0 GCP Trial Suite (current)
│   └── diagrams/
│       ├── v1_architecture.md          # Archived v0.1.x text diagrams
│       ├── v2_architecture.md          # Archived v0.2.0 text diagrams
│       ├── v2_viewer_modules.md        # v0.3.0 viewer internal module map
│       ├── v3_architecture.md          # Archived v0.3.0 text diagrams
│       ├── v4_architecture.md          # Archived v0.4.0 text diagrams
│       └── v5_architecture.md          # Archived v0.5.0 text diagrams
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

# --- v1.0.0 Competition ---
python -m simulation_v2.run_competition
python -m simulation_v2.export_competition --output docs/v10/competition_data.json

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
