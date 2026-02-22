# Prompts

## v0.3.0 Implementation Prompt

> Address the code fix recommendations in kevinkawchak/robot-competition-clinical/blob/main/peer-review/v0.2.1-senior-peer-review.md. Clone the most updated repository. After finishing, document your changes in peer-review, changelog, and releases.
> The current repository needs to provide the full custom clickable urls for the two simulations towards the top of the main Readme. Both of the links are functional.
> https://kevinkawchak.github.io/robot-competition-clinical/
> https://kevinkawchak.github.io/robot-competition-clinical/v2/
>
> Do not change the first simulation. The v2 simulation is far from complete (see attached image). Each of the four stations appear to be hidden inside a large box. The phase timeline and scoreboard overlap other visual elements and need to be closed and re-opened based on user preference. When the four stations finish, it should be clear as to which station finished 1st, 2nd, 3rd, 4th, based on times and accuracies. Everything should be optimized to run on different devices, especially iPhone and android. Update additional relevant elements in Readme such as project structure.
>
> Update the scenario to have the white coat doctor on the left reviewing patient symptoms/toxicities; while the blue coat nurse on the right provides the injection to the patient's arm closest to them. To make this a competition, there needs to be an additional three sets of identical doctor/patient/nurse stations with all medical equipment (all facing the same direction, in a properly spaced 3D 2x2 grid) inside a larger room. Use maximum tokens and processing. Don't stall during processing. All stations need to have separate and simultaneous activity during the competition. Each station competes against each other in time regarding which station is fastest to complete the doctor review followed by the nurse injection. Equally as important, the nurse should be evaluated regarding how accurate the injection was to the patient's arm (how close the syringe needle was to the marked location on the patient's arm).
>
> Update all documentation, readme, text diagrams, etc. to state exactly how the simulation was performed (did each station have the same policy, did each station have a different state, what were the programmed rewards, were all the policies PPO reinforcement learning, how was time and accuracy measured, etc)? Store prior v0.2.0 diagrams and related information as a .md in the docs/diagrams directory. Make certain that the file structure of the first simulation stays intact and distinct from this second simulation, and that the GitHub page links remain distinguishable. Instruct the user on which file(s) need to be uploaded to the simulator for future simulations for the "upload" button in the simulation.
>
> The new simulation should work out of the box. Store this exact prompt in prompts.md under main. Update changelog.md (v0.3.0) and other relevant files under main.
>
> Be sure to fix and address errors that would cause failed checks for the single pull request (such as Python environment issues to avoid the following error during final checks): "3 failing checks
> x Cl / lint-and-format (3.10) (pull...
> x Cl / lint-and-format (3.11) (pull...
> x Cl / lint-and-format (3.12) (pull... " When you are finished, provide a list of new additions and what changed from old to new files. The user will then review your lists prior to committing changes. Perform bug fix, refactor, and migration where appropriate. Provide new release notes in the releases.md folder under main using the format shown below. Separately, provide your processing details shown below.
>
> "FORMAT"
> Release title
> v0.3.0 -
>
> ## Summary
>
> ## Features
>
> ## Contributors
> @kevinkawchak
> @claude
> @codex
>
> ## Notes
> "FORMAT"
>
>
> "PROCESSING"
> [CC_PROCESSING]
> Model: {ID} | API turns: {n}
> Agents spawned: {total} (Bash:{n} Explore:{n} Plan:{n} general-purpose:{n})
> Tool calls: {total} | Read:{n} Edit:{n} Write:{n} Glob:{n} Grep:{n} Bash:{n} WebFetch:{n} WebSearch:{n} Task:{n} TodoWrite:{n}
> Anthropic features: {e.g. extended thinking, tool use, agentic loop, prompt caching}
> Hooks: {active or "none"} | Skills: {invoked or "none"} | Plugins: {used or "none"}
> MCP servers: {count} ({names or "none"})
> Files: read:{n} written:{n} edited:{n} | LOC: +{added} -{removed}
> [/CC_PROCESSING]
>
> Report actual counts. "N/A" if unknown. Do not omit lines.
> "PROCESSING"

## Senior Software Engineer Code Review Prompt (v0.2.1)

You are a senior software engineer that provides comprehensive code reviews to find errors and flaws across the entire kevinkawchak/robot-competition-clinical GitHub codebase. Provide all fixes needed, which will be provided to Claude code to make corrections. Add your code fix recommendations as a new .md to the “peer-review” directory under main. Make sure to resolve the GitHub pages issue so either index.html simulation can be run be run easily and effectively from different directories. Do not fix any code. Make sure to clone from the current repository.

When you are finished, provide a list of new additions and what changed from old to new files. The user will then review your lists prior to committing changes. Provide an update to the changelog (v0.2.1), and add new release notes in the releases.md (v0.2.1) folder using the format below. Include metrics that help track your peer-review process along with your final recommendation metrics (code specifics, number of recommended code fixes, etc.) 

In summary, update the repository (changelog.md, releases.md, peer-review directory and .md) according to your end to end senior software engineer peer review recommendations. A single pull request will be merged by the user at the end. Release notes formatting is shown below. Separately, provide your processing notes as shown below.

“FORMAT”
Release title 
v0.2.1 - 

## Summary

## Features

## Contributors
@kevinkawchak
@codex
@claude

## Notes
“FORMAT”



“PROCESSING”
[CC_PROCESSING]
Model: {ID} | API turns: {n}
Agents spawned: {total} (Bash:{n} Explore:{n} Plan:{n} general-purpose:{n})
Tool calls: {total} | Read:{n} Edit:{n} Write:{n} Glob:{n} Grep:{n} Bash:{n} WebFetch:{n} WebSearch:{n} Task:{n} TodoWrite:{n}
Anthropic features: {e.g. extended thinking, tool use, agentic loop, prompt caching}
Hooks: {active or "none"} | Skills: {invoked or "none"} | Plugins: {used or "none"}
MCP servers: {count} ({names or "none"})
Files: read:{n} written:{n} edited:{n} | LOC: +{added} -{removed}
[/CC_PROCESSING]

Report actual counts. "N/A" if unknown. Do not omit lines.
“PROCESSING”

## Multi-Station Competition Prompt (v0.2.0)

> First, address peer review recommendations in kevinkawchak/robot-competition-clinical/blob/main/peer-review/v0.1.1-senior-peer-review.md. After finishing, document your changes in peer-review, changelog, and releases.
>
> Update the scenario to have the white coat doctor on the left reviewing patient symptoms/toxicities; while the blue coat nurse on the right provides the injection to the patient's arm closest to them. To make this a competition, there needs to be an additional three sets of identical doctor/patient/nurse stations with all medical equipment (all facing the same direction, in a properly spaced 3D 2x2 grid) inside a larger room. Please don't make any shortcuts to the simulation, use max tokens and processing; as all stations need to have separate and simultaneous activity. Each station competes against each other in time regarding which station is fastest to complete the doctor review followed by the nurse injection. Equally as important, the nurse should be measured regarding how quickly and accurate the injection was to the patient's arm. All times and accuracies for all stations should be accessible through simulation control buttons (but not too crowded for mobile phone viewing).
>
> State exactly how the simulation was performed (did each station have the same policy, did each station have a different state, what were the programmed rewards, were all the policies PPO reinforcement learning, how was time and accuracy measured, etc)? Update all documentation, readme, text diagrams, etc. to this new clinical scenario. Make certain that the file structure of the first simulation stays intact and distinct from this second simulation, and that the GitHub page links are distinguishable. Instruct the user on which file(s) need to be uploaded to the simulator for future simulations. Use the existing corresponding GitHub page as a template. Both 1st and 2nd simulation must be separate, and easily accessible through different GitHub page links.
>
> The new simulation should work out of the box. Store the original text diagrams away in a relevant directory, and update the Readme with 3 new comprehensive text based diagrams that discuss features and benefits. Store this exact prompt in prompts.md under main. Update changelog.md (v0.2.0) and other relevant files under main. Clone the most updated repository.
>
> Be sure to fix and address errors that would cause failed checks for the single pull request (such as Python environment issues to avoid the following error during final checks): "3 failing checks
> x Cl / lint-and-format (3.10) (pull...
> x Cl / lint-and-format (3.11) (pull...
> x Cl / lint-and-format (3.12) (pull... " When you are finished, provide a list of new additions and what changed from old to new files. The user will then review your lists prior to committing changes. Perform bug fix, refactor, and migration where appropriate. Provide new release notes in the releases.md folder under main using the format shown below. Separately, provide your processing details shown below.
>
> "FORMAT"
> Release title
> v0.2.0 -
>
> ## Summary
>
> ## Features
>
> ## Contributors
> @kevinkawchak
> @claude
> @codex
>
> ## Notes
> "FORMAT"
>
>
> "PROCESSING"
> [CC_PROCESSING]
> Model: {ID} | API turns: {n}
> Agents spawned: {total} (Bash:{n} Explore:{n} Plan:{n} general-purpose:{n})
> Tool calls: {total} | Read:{n} Edit:{n} Write:{n} Glob:{n} Grep:{n} Bash:{n} WebFetch:{n} WebSearch:{n} Task:{n} TodoWrite:{n}
> Anthropic features: {e.g. extended thinking, tool use, agentic loop, prompt caching}
> Hooks: {active or "none"} | Skills: {invoked or "none"} | Plugins: {used or "none"}
> MCP servers: {count} ({names or "none"})
> Files: read:{n} written:{n} edited:{n} | LOC: +{added} -{removed}
> [/CC_PROCESSING]
>
> Report actual counts. "N/A" if unknown. Do not omit lines.
> "PROCESSING"

## Senior Software Engineer Code Review Prompt (v0.1.1)
You are a senior software engineer that provides comprehensive code reviews to find errors and flaws across the entire kevinkawchak/robot-competition-clinical GitHub codebase. Provide all fixes needed, which will be provided to Claude code to make corrections. Add your code fix recommendations as a new .md to the “peer-review” directory under main. Do not fix any code. Make sure to clone from the current repo state.

When you are finished, provide a list of new additions and what changed from old to new files. The user will then review your lists prior to committing changes. Provide an update to the changelog (v0.1.1), and add new release notes in the releases.md (v0.1.1) folder using the format below. Include metrics that help track your peer-review process along with your final recommendation metrics (code specifics, number of recommended code fixes, etc.) 

In summary, update the repository (changelog.md, releases.md, peer-review directory and .md) according to your end to end senior software engineer peer review recommendations. A single pull request will be merged by the user at the end.

“FORMAT”
Release title 
v0.1.1 - 

## Summary

## Features

## Contributors
@kevinkawchak
@codex
@claude

## Notes
“FORMAT”


Separately, provide your processing details.
[CC_PROCESSING]
Model: {ID} | API turns: {n}
Agents spawned: {total} (Bash:{n} Explore:{n} Plan:{n} general-purpose:{n})
Tool calls: {total} | Read:{n} Edit:{n} Write:{n} Glob:{n} Grep:{n} Bash:{n} WebFetch:{n} WebSearch:{n} Task:{n} TodoWrite:{n}
Anthropic features: {e.g. extended thinking, tool use, agentic loop, prompt caching}
Hooks: {active or "none"} | Skills: {invoked or "none"} | Plugins: {used or "none"}
MCP servers: {count} ({names or "none"})
Files: read:{n} written:{n} edited:{n} | LOC: +{added} -{removed}
[/CC_PROCESSING]

Report actual counts. "N/A" if unknown. Do not omit lines.

## Initial Build Prompt (v0.1.0)

> Build the github repo robot-competition-clinical by comprehensively adding a state of the art simulation based on mujocolab/mjlab (this exact mjlab repo, attribute mjlab). The simulation must utilize g1 robots represented as doctors, nurses, and patients performing tasks such as injecting a patient's upper arm in a specific and appropriate location. Again, there should be elements that this new repo introduces that makes it the next step both technologically and visually over the prior mjlab repo. The patients are in a sitting position who receive the cancer medication. There needs to be a straightforward approach to run and view the baseline simulation from GitHub for many device types, including iOS and android devices. There also needs to be a file upload button for future different uploads, and a play button to view on all devices. Only use fully open and free services throughout (no wandb). The new simulator should work out of the box. Also provide 3 comprehensive text based diagrams in relevant file(s) that discuss features and benefits.
>
> Be sure the simulator can be run easily by the user in 1 or 2 steps from GitHub without terminal. Store this exact prompt in prompts.md under main. Utilize and update changelog.md (v0.1.0) and other relevant files under main.
>
> Be sure to fix and address errors that would cause failed checks for the single pull request (such as Python environment issues to avoid the following error during final checks): "3 failing checks
> x Cl / lint-and-format (3.10) (pull...
> x Cl / lint-and-format (3.11) (pull...
> x Cl / lint-and-format (3.12) (pull... " When you are finished, provide a list of new additions and what changed from old to new files. The user will then review your lists prior to committing changes. Provide new release notes in the releases.md folder under main using the format below. Perform bug fix, refactor, and migration where appropriate.
>
> "FORMAT"
> Release title
> v0.1.0 -
>
> ## Summary
>
> ## Features
>
> ## Contributors
> @kevinkawchak
>
> ## Notes
> "FORMAT"
