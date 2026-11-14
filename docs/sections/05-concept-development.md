---
title: 5. Concept Development and Selection
---
### 5.1. System and Functional Decomposition

The greenhouse microclimate results from interacting thermal loads (solar radiation, air temperature, humidity and leaf temperature) and cooling mechanisms (ventilation and circulation fans, shades, misting and plant transpiration), as mapped in Figure 9. Misting and transpiration cool the air but raise humidity, which limits further evaporative cooling unless the air is exchanged. This coupling is why both temperature and humidity are measured across the greenhouse.

![Figure 9. System decomposition of the greenhouse microclimate](assets/fig-system-decomposition.jpg)

The project objective was decomposed into four functions: acquire, characterise, evaluate and regulate (Figure 10). These map onto the four subsystems in Section 6.

![Figure 10. Functional decomposition of the project objective](assets/fig-functional-decomposition.png)

### 5.2. Concept Selection

The main design decisions were made by comparing alternatives against the constraints in Table 5 (Table 8). The communication choice will be confirmed by benchmarking RS-485 against one wireless option in Semester 2.

[[table: table-concepts | Table 8: Concept selection]]

### 5.3. Simulation-Based Cooling Evaluation

Airflow and heat distribution depend on how cooling equipment is arranged and operated. For example, warm air may accumulate under the roof through buoyancy (Figure 11). A roof vent could release it; an extraction fan could remove it, but only if replacement air can enter lower down; and a circulation fan could break up stagnant air but might push warm air down onto the crops. Which option works depends on the resulting airflow, which is hard to predict without simulation.

![Figure 11. Example: options for warm air trapped under the roof](assets/fig-trapped-hot-air.png)

Testing many configurations physically would be slow and costly. CFD is therefore used to compare fan numbers, positions, orientations and speeds against the baseline, with the greenhouse structure held fixed (Table 9). Configurations are ranked by crop-zone exceedance and fan power. The result is the best-performing configuration among those evaluated, not a mathematical optimum. Two or three of the best configurations will then be tested physically to validate the predictions.

[[table: table-sim-scope | Table 9: Scope of the CFD configuration study]]

> TODO: Confirm the assumption in Table 9: existing ventilation and ceiling fans are modelled as fixed baseline operation, and the floor fans are the configurations being varied.
