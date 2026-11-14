---
title: 3. Problem Statement, Objectives and Scope
---
### 3.1. Problem Statement

> **How might we enable data-informed design and environmental control of tropical greenhouses to improve thermal performance and cooling effectiveness?**

The lack of spatially resolved environmental data and validated thermal models limits the ability to evaluate greenhouse cooling configurations and to apply cooling where crops need it. This project develops a thermal digital twin of GH1, built from site data and updated by a distributed sensor grid. It is used in two ways: to compare fan configurations in simulation before they are installed, and to monitor crop-zone conditions and automate floor-fan cooling, shown on a dashboard.

Success is measured as improvement over GH1's current operation (the baseline), not as reaching an optimal temperature. Holding 24–29 °C at peak sun is not achievable without air-conditioning, whose running cost would outweigh the value of the crops.

### 3.2. Value to Farmers

Farmers do not need the coolest greenhouse; they need a profitable one. The solution must balance three factors (Figure 7): crop-zone thermal performance, the operating cost of cooling, and the value of the crop. Cooling only where crops are growing, and only when needed, aims to reduce fan energy compared with running all fans continuously, while keeping crop hotspots in check. Fan energy and hotspot reduction will be measured directly. Effects on yield, taste and profit are expected long-term benefits that would need agricultural trials beyond this project.

![Figure 7. Farmer desirability: balancing thermal performance, operating cost and crop value](assets/fig-farmer-value.png)

### 3.3. Objectives

1. **O1 Thermal characterisation:** develop a durable distributed sensor network that maps crop-zone thermal conditions in GH1 and provides data for model validation.
2. **O2 Thermal modelling and design evaluation:** develop a CFD model of GH1 and use it to compare fan numbers, positions, orientations and speeds against the current layout.
3. **O3 Digital twin and environmental control:** combine live measurements with the model to show conditions on a dashboard and automatically operate floor fans in response to crop-zone hotspots.

The objectives follow the sequence measure → model → evaluate → monitor → control. Table 4 links each objective to the problem it addresses and the requirements used to test it (Section 4).

[[table: table-problem-solution | Table 4: Target problems, solutions and objectives]]

### 3.4. Scope of Work

Table 5 separates what this project commits to deliver in CDE4301 from the long-term application and from stretch goals. The greenhouse structure is fixed; only fans are varied.

[[table: table-scope | Table 5: Scope of work]]

**Out of scope:** changes to GH1's structure, vents, misting or shading; guaranteeing crop-optimal temperatures at peak sun; air-conditioning; proving yield or profit improvement; and high-accuracy weather or temperature forecasting.

### 3.5. Constraints

The solution must work within the constraints in Table 6, each of which shapes the design.

[[table: table-constraints | Table 6: Design constraints and their implications]]
