---
title: 7. Problems, Shortcomings and Plan
---
### 7.1. Problems Encountered

During MLX90640 development, I²C bus-busy timeouts and EEPROM initialisation failures stopped the camera from returning frames. These were resolved, and complete frames are now transmitted reliably over RS-485. Solar heating of the SHT45 produced a 4.3 °C bias, which led to the shielded enclosure design.

> TODO: Add what caused the I²C problems and how they were fixed (one sentence).

### 7.2. Current Shortcomings

- Only one prototype node has been built; multi-node addressing is not yet implemented.
- Persistent storage and complete Node-RED processing flows are not yet in place.
- The survey method was not fully documented, so the survey needs repeating.
- The shielded enclosure's bias (+1.6 °C) rests on three readings and is still above the R2 target.
- Floor fans have not been procured, and their speed control and power interface are undecided.
- The node power supply (wired DC or battery) is undecided.

### 7.3. Scope of Work

Table 14 sets out what this project will deliver, alongside the long-term application and stretch goals. Only fans are varied; the greenhouse structure stays fixed. Physical tests use four floor fans in the germination section.

[[table: table-scope | Table 14: Scope of work]]

**Out of scope:** changes to GH1's structure, vents, misting or shading; guaranteeing crop-optimal temperatures at peak sun; air-conditioning; proving yield or profit improvement; and developing weather forecasts (NEA data is used as an input).

### 7.4. Plan and Milestones

Work continues from November 2026 to April 2027, with sensing, simulation and control running in parallel (Figure 20). Each milestone has a deliverable and an acceptance criterion (Table 15).

![Figure 20. Project roadmap, November 2026 to April 2027](assets/fig-roadmap.png)

[[table: table-milestones | Table 15: Milestones and acceptance criteria]]
