# Original Architecture Diagrams (v0.1.x)

These diagrams were the original architecture documentation for the v0.1.x
single-station clinical injection simulation. They have been preserved here
for reference. The main README now contains updated diagrams for v0.2.0.

## Diagram 1: System Architecture (v0.1.x)

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

## Diagram 2: Clinical Injection Workflow (v0.1.x)

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

## Diagram 3: Technology Stack and Feature Map (v0.1.x)

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
