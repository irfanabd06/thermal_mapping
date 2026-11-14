---
title: 3. Problem Statement, Objectives and Scope
---
### 3.1. Problem Statement

Tropical greenhouses such as GH1 cannot be held at crop-optimal temperatures at all times without costly active cooling. Within those limits, their fans and vents are placed and operated without spatial analysis or timing logic, and they run continuously. This project develops a thermal digital twin of GH1, built from site data and updated by real-time sensors, to determine **where** cooling equipment should be placed and **when** it should run. The aim is to minimise hotspots and temperature non-uniformity, and then fan energy and cost. Physical fan actuation is used to validate the twin's predictions.

### 3.2. Target Problems and Solutions

Table 2 maps each target problem to one solution, one objective and the requirements used to test it.

[[table: table-problem-solution | Table 2: Target problems, solutions and objectives]]

### 3.3. Objectives

1. **O1 Spatial monitoring:** deploy a calibrated sensor network in a test section of GH1.
2. **O2 Validated model:** build a CFD model of the test section and validate it against measurements.
3. **O3 Placement (where):** compare fan and vent configurations in simulation and recommend a placement for GH1.
4. **O4 Timing (when):** develop fan scheduling on the Raspberry Pi 5 and validate it with physical fans against continuous operation.

### 3.4. Scope and Constraints

Actuation is limited to floor circulation fans procured by the project, so the farm's existing ventilation, misting and shading are not modified. The simulation can still evaluate vents, roof openings and existing fan positions. Bringing GH1 to crop-optimal temperature at all times is out of scope, as it is not achievable without active cooling such as air-conditioning.

> TODO: **To add:** constraints list (physical, environmental, connectivity, power, operational, cost) and the test-section definition.
