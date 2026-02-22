# v2 Viewer Internal Module Map (v0.3.0)

Compact architecture map for the competition viewer (`docs/v2/index.html`).
The viewer is a single HTML file for zero-build deployment, but logically
organizes into the following internal modules.

## Module Dependency Map

```
┌─────────────────────────────────────────────────────────────┐
│              docs/v2/index.html (Single File)               │
│              ~700 lines, Three.js r169 + ES modules         │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─── NAV ────────────────────────────────────────────────┐ │
│  │ Base-path resolver                                     │ │
│  │ Cross-viewer links (root ↔ /v2/)                       │ │
│  └────────────────────────────────────────────────────────┘ │
│          │                                                   │
│  ┌─── CONSTANTS ──────────────────────────────────────────┐ │
│  │ ROOM_W/D/H, GRID_X/Z                                  │ │
│  │ STATION_CONFIGS (name, seed, speed, grid pos, color)   │ │
│  │ DOCTOR_PHASES (4), NURSE_PHASES (6)                    │ │
│  └────────────────────────────────────────────────────────┘ │
│          │                                                   │
│  ┌─── RNG ────────────────────────────────────────────────┐ │
│  │ mulberry32(seed) — deterministic PRNG                  │ │
│  │ ppoJitter(rng, base, speed) — PPO timing noise         │ │
│  └────────────────────────────────────────────────────────┘ │
│          │                                                   │
│  ┌─── RENDERER SETUP ────────────────────────────────────-┐ │
│  │ WebGLRenderer (antialias, PCFSoftShadowMap, ACES)      │ │
│  │ PerspectiveCamera + OrbitControls                       │ │
│  │ Lighting: Ambient + Directional + Hemisphere + Point    │ │
│  └────────────────────────────────────────────────────────┘ │
│          │                                                   │
│  ┌─── SCENE BUILDERS ────────────────────────────────────-┐ │
│  │ buildRoom()      — floor, walls, ceiling, grid          │ │
│  │ buildHumanoid()  — torso, head, legs, arms (L/R pivot)  │ │
│  │ buildPatient()   — chair + seated humanoid + target      │ │
│  │ buildIV/Tray/Monitor/Syringe/Chart() — equipment        │ │
│  │ buildStation()   — complete station with all entities    │ │
│  │ makeLabel()      — canvas-based station name sprite      │ │
│  └────────────────────────────────────────────────────────┘ │
│          │                                                   │
│  ┌─── TIMING ENGINE ─────────────────────────────────────-┐ │
│  │ Per-station PPO-jittered phase boundaries               │ │
│  │ rebuildTiming() — recalculate after config upload        │ │
│  │ finishCount + finishOrder tracking                      │ │
│  └────────────────────────────────────────────────────────┘ │
│          │                                                   │
│  ┌─── ANIMATION ──────────────────────────────────────────┐ │
│  │ animStation(st, dt) — per-station doctor/nurse motion   │ │
│  │ Doctor phases: receive→review→assess→approve            │ │
│  │ Nurse phases: prepare→approach→position→inject→hold→wd  │ │
│  │ smoothstep interpolation: ss(t) = t²(3-2t)             │ │
│  └────────────────────────────────────────────────────────┘ │
│          │                                                   │
│  ┌─── UI PANELS ──────────────────────────────────────────┐ │
│  │ updateScoreboard() — ranked station metrics             │ │
│  │ updatePhaseIndicator() — phase dot progress             │ │
│  │ showFinalResults() — 1st/2nd/3rd/4th overlay            │ │
│  │ Toggle buttons: phases panel, scoreboard panel          │ │
│  │ Station selector: Overview / A / B / C / D              │ │
│  └────────────────────────────────────────────────────────┘ │
│          │                                                   │
│  ┌─── IO ─────────────────────────────────────────────────┐ │
│  │ File upload: JSON parse + schema validation             │ │
│  │ Config application: speed/seed per station              │ │
│  └────────────────────────────────────────────────────────┘ │
│          │                                                   │
│  ┌─── CAMERA ─────────────────────────────────────────────┐ │
│  │ camTgt[overview/0/1/2/3] — preset camera positions      │ │
│  │ startCamAnim() — smooth cubic ease transition           │ │
│  │ ease(t) = 4t³ or 1-(-2t+2)³/2                          │ │
│  └────────────────────────────────────────────────────────┘ │
│          │                                                   │
│  ┌─── MAIN LOOP ─────────────────────────────────────────-┐ │
│  │ animate() — requestAnimationFrame loop                  │ │
│  │ Camera transition + OrbitControls update                 │ │
│  │ Per-station animation (independent, simultaneous)       │ │
│  │ Throttled UI updates (~10Hz)                            │ │
│  │ Auto-pause + results display when all complete          │ │
│  └────────────────────────────────────────────────────────┘ │
│                                                             │
│  CSS: ~150 lines                                            │
│  │ Responsive: 3 breakpoints (default, 768px, 420px)       │
│  │ Dark theme: #0f0f1e base, #00d4ff accent                │
│  │ Panel toggle: visible class, smooth transitions         │
│  │ Final results: fixed overlay with rank badges            │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Data Flow

```
User clicks Play
       │
       ▼
   clock.getDelta()
       │
       ▼
   ┌──────────────────────────────┐
   │ For each station (parallel): │
   │   elapsed += dt              │
   │   find current phase         │
   │   animate doctor/nurse arms  │
   │   track finish order         │
   └──────────────────────────────┘
       │
       ▼
   Update scoreboard + phases (~10Hz)
       │
       ▼
   All stations done?
       │ yes
       ▼
   Show final results overlay
   (1st/2nd/3rd/4th by finish order)
```
