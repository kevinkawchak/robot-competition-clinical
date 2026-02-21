"""Multi-station clinical robot competition simulation (v0.2.0).

Four doctor/patient/nurse stations compete in a 2x2 grid layout.
Each station uses a PPO-trained policy controlling the nurse injection task.
The doctor reviews symptoms/toxicities on the left; the nurse on the right
administers the injection to the patient's nearest arm.

For the single-station simulation, see the simulation package.
"""
