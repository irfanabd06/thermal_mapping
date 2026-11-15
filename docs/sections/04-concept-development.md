---
title: 4. Concept Development and Selection
---
### 4.1. Functional and System Decomposition

Each objective was broken down into the functions a solution must perform (Figure 10). O1 requires conditions to be measured at crop height, captured at the same time, cleaned and mapped to locate hotspots. O2 requires airflow and heat distribution to be estimated for different fan configurations and compared with the baseline. O3 requires hotspots to be forecast, a cooling action decided, fans operated and the response checked.

![Figure 10. Functional decomposition of the objectives, with the requirements that test each one](assets/fig-functional-decomposition.png)

These functions act on the greenhouse system (Figure 11). Sun, outside wind and crop transpiration cannot be controlled; the structure, shading, misting and existing fans stay fixed; floor-fan airflow is the one lever. Temperature, humidity and leaf temperature can be measured directly, but airflow cannot easily be measured, so it must be estimated. Section 5 sets requirements for each function.

![Figure 11. System decomposition: what the solution can and cannot influence, and how heat moves in GH1](assets/fig-system-decomposition.png)

### 4.2. Concept Selection

For each function in Figure 10, alternatives were compared against the constraints in Table 5 (Table 6). The communication choice will be confirmed by benchmarking RS-485 against one wireless option in Semester 2.

[[table: table-concepts | Table 6: Concept selection]]

### 4.3. Simulation-Based Cooling Evaluation

Airflow and heat distribution depend on how cooling equipment is arranged and operated. For example, warm air may accumulate under the roof through buoyancy (Figure 12). A roof vent could release it; an extraction fan could remove it, but only if replacement air can enter lower down; and a circulation fan could break up stagnant air but might push warm air down onto the crops. Which option works depends on the resulting airflow, which is hard to predict without simulation.

![Figure 12. Example: options for warm air trapped under the roof](assets/fig-trapped-hot-air.png)

Testing many configurations physically would be slow and costly. CFD is therefore used to compare fan numbers, positions, orientations and speeds against the baseline, with the greenhouse structure held fixed (Table 7). Configurations are ranked by crop-zone exceedance and fan power. The result is the best-performing configuration among those evaluated, not a mathematical optimum. The model is first checked against floor-fan tests in the germination section, which also supply training data for the digital twin, so both are tested together.

[[table: table-sim-scope | Table 7: Scope of the CFD configuration study]]

> TODO: Confirm the assumption in Table 7: existing ventilation and ceiling fans are modelled as fixed baseline operation, and the floor fans are the configurations being varied.
