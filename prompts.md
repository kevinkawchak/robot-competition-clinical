# Prompts

## v0.9.0 Implementation Prompt

Your goal is to generate a fully functional simulation based on the best performing v0.6.0 Competition from kevinkawchak/robot-competition-clinical. Create a new v0.9.0 link at the top of the current GitHub version table. Keep version labeling based on the current ascending versioning method. There are many issues to fix from v0.6.0 including:
1. The patients do not sit on the chair and their feet is on the seat.
2. The patients' heads are on reverse. The patients don't have facial features.
3. It is not possible to zoom in closely to each station.
4. The tops of the doctors and nurses shoulders appear to have continual resolution/glitching issues.
5. For the person injecting the medicine, the needle does not touch the patient's arm.
Use kevinkawchak/robot-competition-clinical/blob/main/[prompts.md](http://prompts.md) to gain additional feedback, but use v0.6.0 as the most working simulation to based your improvements on.

Place the new release notes in [releases.md](http://releases.md) under main using the format below.
Provide an updated changelog (v0.9.0). Provide a copy of this prompt under [prompts.md](http://prompts.md). When you are finished, auto-push the update to GitHub on your own for my review. The user will then review your updates in GitHub prior to finalization.

"FORMAT"
Release title v0.9.0 -

## Summary

## Features

## Contributors
@kevinkawchak
@claude

## Notes

## v0.8.0 Implementation Prompt

Create v0.8.0 for robot-competition-clinical repo. New simulation that doesn't look/behave like prior versions. SOTA Unitree G1 robots as doctor and nurse. Realistic human patients properly sitting in chairs. Keep time/accuracy competition approach. Keep iPhone/device compatibility, retractable menus, action buttons. Nav banner: "v0.1.0", "0.5.0", "0.6.0", "0.7.0", "0.8.0 (new)" (all clickable). Default view is v0.8.0. Real life hospital equipment. Premium dark theme with frosted glass UI panels and neon cyan accents. PBR-style materials with specular highlights on G1 bodies, translucent IV bags. Enhanced G1 robots with articulated finger segments, battery pack, spine LED strip, ankle actuators. Realistic human patients with hospital wristband, pulse oximeter, visible arm veins, individual fingers. Surgical overhead spotlights with visible glow cones per station quadrant. Glass observation window, curtain dividers between station pairs. Emergency exit sign, wall-mounted hand sanitizer dispensers. Doctor holds alcohol swab in left hand during preparation phase. Nurse wears stethoscope around neck, pen in coat pocket. 18m x 18m room with 6.0m grid spacing. Update README, releases.md, changelog.md, prompts.md. When finished, auto-push to GitHub for review.

## v0.7.0 Implementation Prompt

Improve competition visuals for robot-competition-clinical v0.7.0 building on v0.6.0. Enhancements: (1) Hospital environment — add ceiling with light fixtures over each station quadrant, baseboards along walls, wooden door with frame and handle. (2) Patient facial features — eyes with pupils, eyebrows, nose, mouth on the human patient model. (3) G1 robot torso segmentation — split into chest and abdomen with metallic seam joint. (4) Active nurse animation — nurse G1 should animate throughout all 7 phases, not just monitoring. (5) Patient reactions — head turns toward doctor during injection, hand grip tightens. (6) Nurse LED visor pulse. (7) Updated 4-version nav banner across all viewers. Update all version strings, README, changelog, releases, and prompts. Push to GitHub for review.

## v0.6.0 Implementation Prompt

Your goal in robot-competition-clinical is to create a new v0.6.0 that represents a more visually accurate and appealing competition than v0.5.0 using realistic Unitree G1 robots as the doctors and nurses (from this exact GitHub author: unitreerobotics; not basic robots with limited DOFs), and a realistic human patient receiving the injection. The objective is to illustrate that having competitions like this across multiple robots is advantageous for making future fully autonomous physical ai oncology trials faster than current human trials. Respond "STOP" initially if you cannot implement the G1 robot before proceeding. Remove previous auto memories you have of this repo, and start fresh with this prompt and existing repo contents. Use the full Opus 4.6 1M context length to generate the fixes. Provide the exact number of tokens you used at the end; do not limit inference time or inference time compute.

The prior v0.5.0 competition details regarding factors affecting how times and accuracies are scored appear correct. Refer to the prior version and main robot-competition-clinical if you need assistance with competition details and its PPO mechanics. Keep current functionality for iPhone (and other devices). The retractable menus, and user action buttons work. Abbreviate the top title to now say exactly "v0.1.0", "0.5.0", and now "v0.6.0 (current)" (all clickable which opens their respective version. The default view is v0.6.0 on the most right). Currently, issues in v0.5.0 include the patient has no arms, sits in the chair in reverse, their legs extend through the back of the chair; the red injection target is not on the patient, movements for doctors and nurses are coarse, the doctor isn't actually holding the needle, etc. The hospital equipment needs to stay. The "Station A" and for other stations above their heads is too high. Again, you will have to use your full 1M context length to be able to fix these errors, and provide a correct SOTA simulation.

Make sure v0.6.0 updates show up prominently on Readme and other relevant documentation. Update the table with the new versions that includes the prior release links. Make sure to clone the current repo and utilize appropriate information regarding this pdf. Place the new release notes in releases.md under main using the format below.

Provide an updated changelog (v0.6.0). Provide a copy of this prompt under the prompts.md. When you are finished, auto-push the update to GitHub on your own for my review. The user will then review your updates in GitHub prior to finalization.

"FORMAT"
Release title
v0.6.0 -

## Summary

## Features

## Contributors
@kevinkawchak
@claude

## Notes

## v0.5.0 Implementation Prompt

Clone the most updated kevinkawchak/robot-competition-clinical repository. Move prior v0.4.0 docs and diagrams to a .md in docs/diagrams. Update Readme, diagrams, project structure, etc. to reflect your new v0.5.0. The new simulation should have links to v0.1.0 and v0.5.0 at the top (use only the versions IDs listed in this sentence). Keep the competition theme and light mode visualizations for v0.5.0. Remove the top off of the building to see through. Your latest simulation stations should be as detailed in robots and props and as correctly functional as in v0.1.0 (used as the template)(make sure v0.5.0 contains 4 of the exact stations and human robots used in v0.1.0). Test and run the simulation on your own. Provide results of the simulations you run. Keep the layout and buttons.

Use maximum tokens and processing. Don't stall without updates during processing. Update all documentation, changelog, readme, text diagrams, etc. to state exactly how the simulation was performed (did each station have the same policy, did each station have a different state, what were the programmed rewards, were all the policies PPO reinforcement learning, how was time and accuracy measured, etc)?

The new simulation should work out of the box. Store this exact prompt in prompts.md under main. Update changelog.md (v0.5.0) and other relevant files under main.

Be sure to fix and address errors that would cause failed checks for the single pull request (such as Python environment issues to avoid the following error during final checks): "3 failing checks
x Cl / lint-and-format (3.10) (pull...
x Cl / lint-and-format (3.11) (pull...
x Cl / lint-and-format (3.12) (pull... " When you are finished, provide a list of new additions and what changed from old to new files. The user will then review your lists prior to committing changes. Provide new release notes in the releases.md folder under main using the format shown below.

"FORMAT"
Release title
v0.5.0 -

## Summary

## Features

## Contributors
@kevinkawchak
@claude
@codex

## Notes

## v0.4.0 Implementation Prompt

Clone the most updated kevinkawchak/robot-competition-clinical repository. Fix all GitHub pages links and versions issue (v0.3.0 link is v3 for GitHub.io) Move prior v0.2.0/v0.3.0 docs and diagrams to a .md in docs/diagrams. Update Readme, diagrams, project structure, etc. for your new v0.4.0. The new simulation should have links to both the stable v0.1.0 and the new v0.4.0 at the top. Use light mode visualizations for v0.4.0 to make zooming into each station easier to find. Your latest simulation took shortcuts regarding the simulated robots (degrees of freedom were reduced),  both hospital setting and props were simplified. Also you need to make sure the orientation of each participant in every station is pointing in the same direction as in v0.1.0. Each station should be as detailed and functional as in v0.1.0. Test and run the simulation on your own. Provide results of the simulations you run. Keep the layout and buttons, except for the metrics aren't resetting between runs, and instead of close and replay, it should just show results to close out of (and user can manually replay).

Use maximum tokens and processing. Don't stall without updates during processing, instead provide updates. All stations need to have separate and simultaneous activity during the competition. Each station competes against each other in time regarding which station is fastest to complete the doctor review followed by the nurse injection. Equally as important, the nurse should be evaluated regarding how accurate the injection was to the patient's arm (how close the syringe needle was to the marked location on the patient's arm).

Update all documentation, changelog, readme, text diagrams, etc. to state exactly how the simulation was performed (did each station have the same policy, did each station have a different state, what were the programmed rewards, were all the policies PPO reinforcement learning, how was time and accuracy measured, etc)?

The new simulation should work out of the box. Store this exact prompt in prompts.md under main. Update changelog.md (v0.4.0) and other relevant files under main.

Be sure to fix and address errors that would cause failed checks for the single pull request (such as Python environment issues to avoid the following error during final checks): "3 failing checks
x Cl / lint-and-format (3.10) (pull...
x Cl / lint-and-format (3.11) (pull...
x Cl / lint-and-format (3.12) (pull... " When you are finished, provide a list of new additions and what changed from old to new files. The user will then review your lists prior to committing changes.  Perform bug fix, refactor, and migration where appropriate. Provide new release notes in the releases.md folder under main using the format shown below. Again, don't stall without providing text updates throughout your progress.

## v0.3.0 Implementation Prompt

You are an AI assisting with code development. The developer has received a peer review of their project `robot-competition-clinical` and wants to implement all the recommendations. Using the peer review document as your guide, implement all recommended improvements to the `robot-competition-clinical` project, specifically targeting the competition viewer at `docs/v2/index.html` and any supporting files. Do the work yourself without asking the user questions. You must: 1. Read and analyze the peer review document at `peer-review/v0.2.1-senior-peer-review.md` first 2. Systematically implement each recommendation 3. Add tests for new functionality 4. Create an implementation report at `peer-review/v0.3.0-implementation-report.md` 5. Update version to 0.3.0 across all relevant files 6. Commit with a descriptive message and push to a new branch After every file modification, verify your changes are correct. Be thorough and methodical. Do not skip any recommendations unless there's a strong technical reason (document the reason if so). Ask the user zero questions - figure out the right approach yourself and do the best that you can. Take your time to do it correctly.
