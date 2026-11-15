---
title: 4. Concept Development and Selection
---
### 4.1. Functional and System Decomposition

Each objective was broken down into the functions a solution must perform (Figure 10). O1 requires conditions to be measured at crop height, captured at the same time, cleaned and mapped to locate hotspots. O2 requires airflow and heat distribution to be estimated for candidate fan layouts, the best layouts suggested, and their improvement confirmed in real-life tests. O3 requires hotspots to be forecast, a cooling action decided, fans operated and the right fans confirmed to respond.

![Figure 10. Functional decomposition of the objectives, with the requirements that test each one](assets/fig-functional-decomposition.png)

These functions act on the greenhouse system (Figure 11). Sun, outside wind and crop transpiration cannot be controlled; the structure, shading, misting and existing fans stay fixed, with floor-fan airflow as the one lever. Temperature, humidity and leaf temperature can be measured directly, but airflow cannot easily be measured, so it must be estimated. Section 5 sets requirements for each function.

![Figure 11. System decomposition: what the solution can and cannot influence, and how heat moves in GH1](assets/fig-system-decomposition.png)

### 4.2. Concept Selection

For each function in Figure 10, alternatives were compared against the constraints in Table 5 (Table 6). The communication choice will be confirmed by benchmarking serial RS-485 against wireless options.

[[table: table-concepts | Table 6: Concept selection]]

### 4.3. Cooling Layout Evaluation: Why Simulation

Airflow and heat distribution depend on how cooling equipment is arranged. Warm air trapped under the roof, for example, could be released by a vent, removed by an extraction fan if air can enter lower down, or mixed by a circulation fan at the risk of pushing it onto the crops (Figure 12). Which works depends on airflow that is hard to predict.

Additionally, testing many layouts physically is slow and costly. Fan layouts are therefore compared in simulation against the baseline, with the structure fixed, and ranked by crop-zone exceedance and fan power. Farmers building or retrofitting a greenhouse could use the same model to design their fan layout, and the twin then runs on the chosen layout.

![Figure 12. Example: options for warm air trapped under the roof](assets/fig-trapped-hot-air.png)
