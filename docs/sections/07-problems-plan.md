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

This project covers one part of GH1: the 20 m-long germination section, used as the test section. All sensing, mapping, simulation and fan tests take place there, while the full greenhouse is the long-term application (Table 14). Only fans are varied; the greenhouse structure stays fixed.

[[table: table-scope | Table 14: Scope of work]]

**Out of scope:** the rest of GH1 beyond the germination section, apart from the baseline survey and geometry; changes to GH1's structure, vents, misting or shading; guaranteeing crop-optimal temperatures at peak sun; air-conditioning; proving yield or profit improvement; and developing weather forecasts (NEA data is used as an input).

### 7.4. Plan and Milestones

Work continues from November 2026 to April 2027, with sensing, simulation and control running in parallel (Figure 22). Each milestone has a deliverable and an acceptance criterion (Table 15).

![Figure 22. Project roadmap, November 2026 to April 2027](assets/fig-roadmap.png)

[[table: table-milestones | Table 15: Milestones and acceptance criteria]]
