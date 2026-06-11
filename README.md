# Clinical Robot Competition

MuJoCo-based clinical trial simulation with **real Unitree H2 humanoid robots**
(from [unitreerobotics](https://www.unitree.com/)) competing across **four simultaneous
stations** in a 2x2 grid. At each station a **doctor H2** (factory white, red cross) and a
**nurse H2** (scrub-blue shells) execute a complete **GCP-aligned 12-phase intramuscular
injection visit** on a **realistic human trial participant**.

v1.2.0 is the recommended viewer — everything made real life: the robots are the **actual
Unitree H2 Plus model** (visual meshes, all 75 revolute joints, dual SHARPA dexterous hands)
converted offline from `H2_Plus/H2_with_sharpa.usdz` in
[kevinkawchak/fork_unitree_model](https://github.com/kevinkawchak/fork_unitree_model/tree/main/H2_Plus). Built as the next step beyond [mjlab](https://github.com/mujocolab/mjlab)
(mujocolab/mjlab).

## Quick Start (1-2 Steps from GitHub)

**Step 1:** Enable GitHub Pages in your fork:
Settings → Pages → Source: "Deploy from a branch" → Branch: `main`, Folder: `/docs` → Save

**Step 2:** Open the simulation on any device (desktop, iOS, Android):

| Version | URL | Description |
|---|---|---|
| **v1.2.0 Real-Life GCP Suite II (new)** | [https://kevinkawchak.github.io/robot-competition-clinical/v12/](https://kevinkawchak.github.io/robot-competition-clinical/v12/) | Zero object overlaps (rotational arm IK), grasping SHARPA hands, unique per-station choreography, typing CRA, distortion-free signage |
| v1.1.0 Real-Life GCP Suite | [https://kevinkawchak.github.io/robot-competition-clinical/v11/](https://kevinkawchak.github.io/robot-competition-clinical/v11/) | Real Unitree H2 robot files (75 DOF + SHARPA hands), realistic patients, dissimilar station motion/scoring, infinite zoom, daylight open-air suite |
| v1.0.0 GCP Trial Suite | [https://kevinkawchak.github.io/robot-competition-clinical/v10/](https://kevinkawchak.github.io/robot-competition-clinical/v10/) | 12-phase GCP visit, 43-DOF robots, IK needle contact, composite scoring, open-top photoreal suite, AE response, human CRA |
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

> **If every page returns 404:** first check the serving self-test at
> [`/health.txt`](https://kevinkawchak.github.io/robot-competition-clinical/health.txt).
> If `health.txt` also 404s even though the latest **"pages build and deployment"** run
> under the Actions tab is green, the Pages site routing is stuck and must be re-created
> from the browser: Settings → Pages → set Source to **None** → Save → wait one minute →
> set Source back to **Deploy from a branch** (`main`, `/docs`) → Save. If instead
> `health.txt` loads, the site is fine — a missing path now shows this project's own
> [404 page](docs/404.html) with links to every version.

## Instructions for Claude Code: Adding a New Simulation Version With Zero 404s

> **This section is written for a future Claude Code (or any AI coding agent) session
> asked to build simulation version vX.Y.Z.** Every past 404 on this site came from one
> of the mistakes below — not from GitHub Pages being broken. Follow each rule exactly
> and the new simulation will load on the first try.

1. **Put the page in the one folder that gets served.** GitHub Pages publishes the
   `/docs` folder of the `main` branch only. The new simulation must be a single
   self-contained file at `docs/v<N>/index.html`, where `<N> = major×10 + minor`
   of the release version: v0.5.0 → `v5`, v0.9.0 → `v9`, v1.0.0 → `v10`,
   v1.1.0 → `v11`, v1.2.0 → `v12`. Never place pages at the repository root, never
   invent a different folder scheme, and never rename or move existing `docs/v*` folders.

2. **Know the URL mapping before writing any link.** `docs/v<N>/index.html` is served at
   `https://kevinkawchak.github.io/robot-competition-clinical/v<N>/` — the `docs/`
   segment is **not** part of the URL, paths are case-sensitive, and the folder name,
   README link, and nav links must all use the identical `v<N>`. (The original v0.3.0
   404 happened because content lived in `docs/v2/` while links said `/v3/`.)

3. **All links between pages must be relative.** From the landing page
   (`docs/index.html`) link as `href="v<N>/"`. From one version page to another, reuse
   the existing pattern in every `docs/v*/index.html`: derive the base from
   `window.location.pathname` and append `v<N>/`. Never write root-absolute links like
   `/v<N>/` — the site lives under `/robot-competition-clinical/`, so root-absolute
   links 404 on github.io.

4. **No build step exists — keep it that way.** `docs/.nojekyll` is intentional: Pages
   publishes these files verbatim. Do not delete `.nojekyll`, do not add Jekyll
   front matter, and do not add assets that require compilation. One HTML file with
   inline CSS/JS (CDN `<script>` imports are fine) is the required format.

5. **Nothing is live until it is merged to `main`.** Pushing a feature branch deploys
   nothing, and telling the user a URL works before merge is the second way past
   sessions caused "404" reports. After the merge, the **"pages build and deployment"**
   workflow (Actions tab) must complete green for the merge commit — it usually takes
   under a minute.

6. **Verify in this order before reporting success.**
   1. The "pages build and deployment" run for the merge commit concluded `success`.
   2. The run's **build job log** prints the deployed artifact's file listing — confirm
      `./v<N>/index.html` appears in it.
   3. Fetch `https://kevinkawchak.github.io/robot-competition-clinical/health.txt`,
      then the new `…/v<N>/` URL. **If your environment's network policy blocks
      fetching the live site** (sandboxed Claude Code web sessions usually do — every
      request returns a proxy 403), say so plainly and cite steps 1–2 as your evidence
      instead of claiming you tested the URL.
   4. If the user still reports 404 on every page while step 1–2 pass, the Pages
      routing is stuck on GitHub's side; no commit can fix it. Ask the user to apply
      the Settings → Pages source toggle described in the Quick Start callout above.

7. **Update the companion files in the same change**: add the new row (marked
   "**(new)**") to the README version table and remove "(new)" from the previous row;
   add the version to the nav banner of `docs/index.html` **and every existing**
   `docs/v*/index.html`; append the implementation prompt to `prompts.md`; add entries
   to `changelog.md` and `releases.md` following their existing format; bump the
   version in `pyproject.toml`. Run `ruff check .` and `ruff format --check .` so CI
   passes.

## Simulation Evolution (v0.1.0 → v1.2.0)

Across twelve releases the simulation grew from a demo into a living autonomous clinic. v0.1.0–v0.4.0 (Claude Opus) built a single ~6 m exam bay with one scripted injection visit, then scaled to a 12×12 m, four-station PPO-seeded race scored on time and accuracy. v0.5.0–v0.9.0 (Opus) added light-mode viewing, recognizable Unitree G1 robots, seated patients with faces, close zoom, and needle-contact fixes — roughly 20 animated DOF per robot across four stations in a 16 m hall. v1.0.0 (first Fable 5 build) was a ground-up rebuild for clinical-trial realism: an 18×18 m open-top suite, 43-DOF G1s with dexterous fingers, a 12-phase GCP visit, composite scoring, live ECG, a seeded adverse event, and a human CRA. v1.1.0 swapped in the real 75-DOF Unitree H2 Plus robot files (USD→GLB, dual SHARPA hands), realistic patient personas, infinite zoom, and a 20×20 m daylight suite. v1.2.0 hardens physical truth: rotational arm IK, zero object overlaps, grasping hands, and unique per-station choreography.

## What This Simulates (v1.1.0–v1.2.0)

Four stations compete simultaneously to complete a **GCP-aligned 12-phase IM injection
visit** on diverse, realistic human participants (per-station skin tone, hairstyle, gown
color and persona — calm / talkative / anxious / elderly — with blinking, breathing, consent
nods, chatting, fidgeting, tremor, and armrest grip during injection). The doctor and nurse
are the **real Unitree H2 Plus humanoids**: the actual robot geometry and all **75 revolute
joints (incl. dual SHARPA five-finger dexterous hands)** are converted offline from the
binary-USD robot description in `fork_unitree_model/H2_Plus` into `docs/v11/h2_plus.glb`
(151k triangles, joint axes/limits preserved in node extras), then articulated live in the
browser. A runtime **IK tip-correction** servo drives the needle tip onto the deltoid target
every frame — touching the surface at insertion and sitting indwelling during the slow-push
dose — with zero interpenetration. **No two stations move alike**: each seed draws a motion
style (stride, cadence, lean, reach, head energy, walk-path bow, pose tempo) plus a staggered
visit start, and each profile shapes its metrics (the speed station really is faster and
sloppier; the precision station tighter and more deliberate). One seeded station experiences
a **Grade 1 vasovagal adverse event** during observation (ECG dips to ~49 bpm, patient's head
droops, nurse responds, observation extends). A **human CRA** monitors everything from a
sponsor desk with a live EDC laptop, and a central **4-face scoreboard tower** broadcasts
live ranks. The suite is open-air (no ceiling) under a physically-modeled daylight sky, with
bumper-railed walls, a live wall clock, scrub sink, crash cart, supply shelving, medical-gas
outlets, EXIT signage, plants, an observation window, 4x-resolution auto-fit signage, and
full per-station equipment.

### v1.2.0 Headline Upgrades

| # | Area | v1.2.0 Upgrade |
|---|------|----------------|
| 1 | Physical integrity | Rotational arm IK (CCD over the real H2 shoulder/elbow/wrist axes): the injecting hand stays attached to the wrist and stops at the deltoid surface — no detached hand, no pass-through; soles exactly on the floor; verified cart and monitor work distances |
| 2 | Grasping hands | Open-reach-close pickup of the syringe from the tray, carry grip, release over the sharps chute; palm-up tablet cradle with fingers around the edge; scanner trigger squeezes; idle finger micro-motion |
| 3 | Unique choreography | Per-station personalized pose tables (seeded stance/arm/head offsets) + discrete flavors: 4 hand-hygiene techniques, 3 swab patterns, 3 tap rhythms, arm swing while walking, clamped per-station walk bows |
| 4 | Display integrity | Signage fully inside the wall band (below the cap, above the bumper rail), z-fighting and shadow acne eliminated (no dark/multicolor pixel distortion), tower pole joined to its board |
| 5 | Scene integrity | Plants rooted in their pots, one-piece connected scrub sink, paper-towel dispenser flush on the wall, typing CRA whose hands stay above the desk |

### v1.1.0 Headline Upgrades

| # | Area | v1.1.0 Upgrade |
|---|------|----------------|
| 1 | Real robot files | Actual Unitree H2 Plus geometry + joint tree (75 revolute DOF, dual SHARPA hands) converted from `fork_unitree_model/H2_Plus/H2_with_sharpa.usdz` (binary USD crate) to a 3.7 MB GLB with axes/limits in node extras |
| 2 | Realistic patient | Rebuilt humans: five-finger articulated hands, expressive faces (lids, brows, lips, ears, cheeks), ECG chest leads, reading glasses for the elderly persona, persona-driven idle behavior |
| 3 | Dissimilar stations | Seeded per-station motion style (stride, cadence, lean, reach, head energy, path bow, tempo) + staggered starts + profile-correlated metric draws — movements AND scores differ naturally |
| 4 | Infinite zoom | Fly-through dolly with no min/max distance, zoom-to-cursor, pivot glide-through, adaptive near/far clip planes; works from any point, in and out, through geometry |
| 5 | Signage | All posters/labels/boards re-rendered at 4x resolution with measure-and-fit headings and word-wrapped body text — no clipped headings at any zoom |
| 6 | Real-life suite | Physical daylight sky over the open-top room, wall bumper rails, live wall clock, scrub sink, crash cart, supply shelving, per-station gas outlets, EXIT sign, plants |

### v1.0.0 Headline Upgrades

| # | Area | v1.0.0 Upgrade |
|---|---|---|
| 1 | High-DOF robots | 43 DOF per G1: 7-DOF arms, 7-DOF Dex3-1 hands with 2-segment articulated fingers, 3-DOF waist, 2-DOF neck, 6-DOF legs with gait cycle |
| 2 | Physical overlap | Fixed by construction: coat = torso shell (no overlay z-fight), verified prop clearances, patient soles exactly on floor, props flush on surfaces, IK prevents needle interpenetration |
| 3 | Competition realism | 12-phase GCP workflow, composite GCP scoring, seeded Grade 1 AE with response, live ECG/SpO2/NIBP, eSource documentation, human-in-the-loop CRA |
| 4 | Room | Open-top (no ceiling), photoreal textures, observation window + hallway, posters, privacy screens, exam-light booms, supply carts, sharps containers, scoreboard tower |
| 5 | Zoom | minDistance 0.05 m, zoom-to-cursor, fog removed, double-click/double-tap glide-focus on any object, per-station camera presets, keyboard shortcuts |

### 12-Phase GCP Visit Per Station (v1.1.0)

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

**Total base duration:** 18.5 seconds. PPO jitter, profile tempo and speed profiles produce
actual visit times of ~18.1–21.1 s, plus a seeded 0.7–1.8 s staggered start per station.

### Station Layout (2x2 Grid)

| Station | Position | Seed | Speed | Patient (persona) | Profile | Start stagger |
|---------|----------|------|-------|-------------------|---------|---------------|
| **A** | Front-left | 42 | 1.00x | Light skin, short brown hair, mint gown (calm) | Balanced | 1.75 s |
| **B** | Front-right | 137 | 0.93x | Deep brown skin, black curly hair, light-blue gown (talkative) | Speed-focused | 0.66 s |
| **C** | Back-left | 256 | 1.07x | Tan skin, long dark hair, lavender gown (anxious) | Careful (draws the Grade 1 AE) | 0.77 s |
| **D** | Back-right | 512 | 0.97x | Pale skin, grey bun, peach gown (elderly, glasses) | Precision-focused | 1.16 s |

### Role Assignments (v1.1.0)

| Role | Position | Appearance | Equipment | Action |
|------|----------|------------|-----------|--------|
| Doctor (H2) | Right of patient, walks to cart | Real Unitree H2 Plus, factory white shells, red cross chest plate | Syringe (IK-corrected needle), swab, vial | Hygiene, drug prep, site prep, injection, dose, sharps disposal |
| Nurse (H2) | Left of patient | Real Unitree H2 Plus, scrub-blue shells, gold badge | Tablet (always), wristband scanner | Identity check, eConsent, vitals, observation, eSource documentation |
| Patient (Human) | Infusion recliner, feet on floor | Diverse per station with personas; blinks, breathes, nods, chats, fidgets, grips armrest | Wristband, live ECG chest leads | Receives the 0.50 mL IM dose (right deltoid) |
| CRA (Human) | Sponsor monitoring desk | Business casual, ID badge | EDC laptop, monitoring banner | Human-in-the-loop oversight; types, scans the room |

### Composite GCP Scoring (v1.1.0)

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

**v1.1.0 — seeds you can see**: the same seeds additionally drive a per-station motion style
(stride, cadence, waist lean, arm reach, head energy, walk-path bow, pose tempo, start
stagger) and profile-correlated metric distributions, so the policy differences are visible
in how the robots carry themselves, not just in the score table.

### Simulation Results (v1.1.0–v1.2.0, deterministic from seeds)

| Rank | Station | Composite | Total Time | Needle Dev | Protocol | Sterility | Dose | Motion Style | Notes |
|------|---------|-----------|-----------|------------|----------|-----------|------|--------------|-------|
| #1 | **D** | **96.6** | 18.61s | 0.33mm | 98.8% | 99.1% | 0.499mL | precision | Precision wins |
| #2 | A | 89.0 | 18.77s | 1.99mm | 97.3% | 97.9% | 0.500mL | balanced | Perfect dose |
| #3 | C | 85.6 | 21.08s | 1.80mm | 98.6% | 98.8% | 0.496mL | careful | Grade 1 vasovagal AE, resolved |
| #4 | B | 82.2 | 18.09s | 3.30mm | 96.5% | 97.5% | 0.504mL | speed | Fastest wall finish, ranks last |

**Winner: Station D** — sub-millimeter needle placement at near-best time. Station B is the
first to finish on the wall clock (fastest visit + earliest staggered start) yet places #4:
its speed-profile motion style trades accuracy for tempo, exactly the kind of natural
dissimilarity the composite GCP score is designed to expose.

## Features

- **Zero Object Overlaps** (v1.2.0): rotational arm IK on the real joint axes (no detached
  or pass-through hands), soles on the floor, verified prop clearances, signage inside the
  wall band, rooted plants, connected sink, z-fight/shadow-acne-free surfaces
- **Grasping SHARPA Hands** (v1.2.0): tray pickup, carry, sharps release, palm-up tablet
  cradle, scanner trigger squeezes, idle finger micro-motion
- **Unique Station Choreography** (v1.2.0): per-station personalized pose tables + discrete
  hygiene/swab/tap flavors and walk styles — no two stations move alike
- **Typing CRA** (v1.2.0): hands above the desk, palms over the keyboard, believable taps
- **Real Unitree H2 Robot Files** (v1.1.0): actual H2 Plus geometry + full joint tree (75
  revolute DOF incl. dual SHARPA five-finger hands) converted from
  `fork_unitree_model/H2_Plus/H2_with_sharpa.usdz` to `docs/v11/h2_plus.glb` with joint
  axes/limits in node extras; simplified procedural fallback if the GLB cannot load
- **Realistic Patients v2** (v1.1.0): five-finger hands, expressive faces, ECG chest leads,
  personas (calm / talkative / anxious / elderly) with chatting, fidgeting, tremor, glasses
- **Naturally Dissimilar Stations** (v1.1.0): seeded motion styles (stride, cadence, lean,
  reach, head energy, path bow, tempo), staggered starts, profile-correlated metric draws
- **Infinite Zoom** (v1.1.0): fly-through dolly with no min/max distance, zoom-to-cursor,
  pivot glide-through, adaptive near/far planes — from any point, in and out
- **4x-Resolution Auto-Fit Signage** (v1.1.0): measure-and-fit headings, word-wrapped body,
  framed posters — no clipped or blurry text at any zoom
- **Real-Life Open-Air Suite** (v1.1.0): physical daylight sky (no ceiling), bumper rails,
  live wall clock, scrub sink, crash cart, shelving, gas outlets, EXIT sign, plants
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
- **9-Version Nav Banner**: v0.1.0 | v0.5.0 | … | v1.0.0 | v1.1.0 | v1.2.0 (new)
- **Open & Free**: all dependencies open-source (no wandb)

## Architecture Diagrams

### Diagram 1: Multi-Station Competition Architecture (v1.0.0)

```
+----------------------------------------------------------------------+
|        CLINICAL ROBOT COMPETITION - SYSTEM ARCHITECTURE v1.1.0       |
|   Real-Life GCP Suite: 12-phase visit, 75-DOF H2s, composite score  | 
+----------------------------------------------------------------------+
|                                                                      |
|  +----------------------+        +-------------------------------+   |
|  |  MuJoCo Backend      |        |   Three.js GCP Trial Suite    |   |
|  |  (Python)            |        |   (HTML/JS - docs/v11/)       |   |
|  |                      |        |                               |   |
|  | +------------------+ |  JSON  | +---------------------------+ |   |
|  | | competition_scene| | -----> | | Open-Top Photoreal Room   | |   |
|  | | .xml (4 stations)| | export | | - 20m x 20m, no ceiling   | |   |
|  | +------------------+ |        | | - 8 real H2 robots, 75 DOF| |   |
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
|  H2 Robots: Unitree Robotics via fork_unitree_model/H2_Plus        | 
+----------------------------------------------------------------------+
```

### Diagram 2: GCP Competition Workflow (v1.0.0)

```
+----------------------------------------------------------------------+
|            GCP COMPETITION WORKFLOW - 4-STATION VISIT RACE           |
|   v1.1.0: 12-phase GCP visit, composite scoring, seeded Grade 1 AE   |
+----------------------------------------------------------------------+
|                                                                      |
|  N=nurse  D=doctor                                                   |
|  [identity][consent][vitals][hygiene][drugprep][siteprep][position]  |
|     N         N        N       D         D         D        D       |
|  [inject][dose][withdraw][sharps][monitor+eSource]                   |
|     D      D       D        D        N                               |
|                                                                      |
|  STATION A (seed=42,  1.00x): 18.77s  1.99mm  composite 89.0  #2    |
|  STATION B (seed=137, 0.93x): 18.09s  3.30mm  composite 82.2  #4    |
|  STATION C (seed=256, 1.07x): 21.08s  1.80mm  composite 85.6  #3    |
|             ^ Grade 1 vasovagal AE during monitor (+2.5s/speed)      |
|  STATION D (seed=512, 0.97x): 18.61s  0.33mm  composite 96.6  #1    |
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
|  |   #1  Station D - 96.6 - 18.61s - 0.33mm  (precision wins)      | |
|  |   #2  Station A - 89.0 - 18.77s - 1.99mm                        | |
|  |   #3  Station C - 85.6 - 21.08s - 1.80mm  (AE Gr.1, resolved)   | |
|  |   #4  Station B - 82.2 - 18.09s - 3.30mm  (fastest, ranks last) | |
|  |           [ Close Results ]  <- user manually replays           | |
|  +-----------------------------------------------------------------+ |
+----------------------------------------------------------------------+
```

### Diagram 3: v1.0.0 3D Layout and Technology Stack

```
+----------------------------------------------------------------------+
|     3D LAYOUT & TECHNOLOGY STACK (v1.1.0 - Real-Life GCP Suite)     | 
+----------------------------------------------------------------------+
|                                                                      |
|  +------- OPEN-TOP SUITE (20m x 20m, NO CEILING) -----------------+  |
|  |   obs window--+                                                |  |
|  |  +-- Station A ---------+    +-- Station B ---------+          |  |
|  |  | [H2n] [Pat] [H2d]    |    | [H2n] [Pat] [H2d]    |          |  |
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
|  Legend: H2d=Doctor(white H2 Plus, red cross, syringe w/ IK, R)     | 
|          Pat=Patient(diverse personas, ECG leads, soles on floor)   | 
|          H2n=Nurse(scrub-blue H2 Plus shells, tablet+scanner, L)    | 
|                                                                      |
|  LAYER 1: MuJoCo + PPO (Python backend)                              |
|  LAYER 2: Three.js r169 (docs/v11/) + Sky daylight + GLB H2 robots  | 
|  LAYER 3: GitHub Pages (static hosting)                              |
|                                                                      |
|  OPEN-SOURCE: MuJoCo(Apache2) Three.js(MIT) Python(PSF) Ruff(MIT)    |
|  ROBOTS: Unitree H2 Plus (unitreerobotics) via fork_unitree_model   | 
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
│   │   └── index.html                  # v1.0.0 GCP Trial Suite
│   ├── v11/
│   │   ├── index.html                  # v1.1.0 Real-Life GCP Suite
│   │   └── h2_plus.glb                 # Real Unitree H2 Plus model (from H2_Plus USD)
│   ├── v12/
│   │   ├── index.html                  # v1.2.0 Real-Life GCP Suite II (current)
│   │   └── h2_plus.glb                 # Same H2 Plus model (self-contained folder)
│   └── diagrams/
│       ├── v1_architecture.md          # Archived v0.1.x text diagrams
│       ├── v2_architecture.md          # Archived v0.2.0 text diagrams
│       ├── v2_viewer_modules.md        # v0.3.0 viewer internal module map
│       ├── v3_architecture.md          # Archived v0.3.0 text diagrams
│       ├── v4_architecture.md          # Archived v0.4.0 text diagrams
│       └── v5_architecture.md          # Archived v0.5.0 text diagrams
├── tools/
│   └── convert_h2_usd_to_glb.py        # Offline H2_Plus USDZ -> docs/v11/h2_plus.glb
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

**Unitree H2 robot model**: the v1.1.0 robots are converted from
[`kevinkawchak/fork_unitree_model`](https://github.com/kevinkawchak/fork_unitree_model/tree/main/H2_Plus)
(`H2_Plus/H2_with_sharpa.usdz`, a fork of Unitree Robotics'
[unitree_model](https://github.com/unitreerobotics/unitree_model) — BSD-3-Clause), using
`tools/convert_h2_usd_to_glb.py`. Robot design © Unitree Robotics.

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
