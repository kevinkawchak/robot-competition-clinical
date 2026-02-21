# Prompts

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
