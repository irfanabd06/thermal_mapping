---
title: 4. Concept Development and Selection
---
### 4.1. Functional and System Decomposition

Each objective was broken down into the functions a solution must perform (Figure 10). O1 requires conditions to be measured at crop height, captured at the same time, cleaned and mapped to locate hotspots. O2 requires airflow and heat distribution to be estimated separately for different fan configurations and compared with the baseline. O3 requires hotspots to be forecast, a cooling action decided, fans operated and the response checked.

![Figure 10. Functional decomposition of the objectives, with the requirements that test each one](assets/fig-functional-decomposition.png)

These functions act on the greenhouse system (Figure 11). Sun, outside wind and crop transpiration cannot be controlled; the structure, shading, misting and existing fans stay fixed, with floor-fan airflow as the one lever. Temperature, humidity and leaf temperature can be measured directly, but airflow cannot easily be measured, so it must be estimated. Section 5 sets requirements for each function.

![Figure 11. System decomposition: what the solution can and cannot influence, and how heat moves in GH1](assets/fig-system-decomposition.png)

### 4.2. Concept Selection

For each function in Figure 10, alternatives were compared against the constraints in Table 5 (Table 6). The communication choice will be confirmed by benchmarking serial RS-485 against wireless options.

[[table: table-concepts | Table 6: Concept selection]]

### 4.3. Cooling Layout Evaluation

Airflow and heat distribution depend on how cooling equipment is arranged and operated. For example, warm air may accumulate under the roof through buoyancy (Figure 12). A roof vent could release it; an extraction fan could remove it, but only if replacement air can enter lower down; and a circulation fan could break up stagnant air but might push warm air down onto the crops. Which option works depends on the resulting airflow, which is hard to predict without simulation. As the structure is fixed in this project, only fan options are evaluated.

![Figure 12. Example: options for warm air trapped under the roof](assets/fig-trapped-hot-air.png)

Testing many layouts physically would be slow and costly. CFD therefore estimates airflow, and heat distribution for layouts not yet installed, using measured inputs such as roof temperature and fan flow (Table 7). Fan number, position, direction and speed are compared against the baseline and ranked by crop-zone exceedance and fan power, giving the best layout among those evaluated rather than a mathematical optimum. Because conditions change quickly, the model is judged on trends and rankings, not absolute temperatures (R7). It is first checked against floor-fan tests in the germination section, which also supply measured heat distribution and training data for the data-driven twin, so both are tested together.

[[table: table-sim-scope | Table 7: Scope of the CFD configuration study]]
