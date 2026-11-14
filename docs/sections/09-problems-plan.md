---
title: 9. Problems, Shortcomings and Plan
---
### 9.1. Problems Encountered

During MLX90640 development, I²C bus-busy timeouts and EEPROM initialisation failures stopped the camera from returning frames. These were resolved, and complete frames are now transmitted reliably over RS-485. Solar heating of the SHT45 produced a 4.3 °C bias, which led to the shielded enclosure design.

> TODO: Add what caused the I²C problems and how they were fixed (one sentence).

### 9.2. Current Shortcomings

- Only one prototype node has been built; multi-node addressing is not yet implemented.
- Persistent storage and complete Node-RED processing flows are not yet in place.
- The survey method was not fully documented, so the survey needs repeating.
- The shielded enclosure's remaining bias has not been quantified.
- Floor fans have not been procured, and their speed control and power interface are undecided.
- The node power supply (wired DC or battery) is undecided.

### 9.3. Plan and Milestones

Work continues from November 2026 to April 2027, with sensing, simulation and control running in parallel (Figure 18). Each milestone has a deliverable and an acceptance criterion (Table 13).

![Figure 18. Project roadmap, November 2026 to April 2027](assets/fig-roadmap.png)

[[table: table-milestones | Table 13: Milestones and acceptance criteria]]
