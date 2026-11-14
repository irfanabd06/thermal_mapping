---
title: 4. Design Specifications
---
### 4.1. Baseline-Referenced Validation

This project focuses on comparative evaluation rather than reaching optimal conditions. Results depend on the weather: on very hot days, crop temperatures cannot be brought down to the optimal range, and passing clouds, wind and misting disturb every measurement. Each solution is therefore compared against a reference baseline: GH1's current operation, with existing fans running continuously, measured under comparable weather. The requirements ensure that measurement error is small enough for those comparisons to be meaningful.

Hotspots are judged only where crops grow, using a crop-zone exceedance index for each zone *i*:

<p class="equation">H<sub>i</sub> = A<sub>i</sub> · max(0, T<sub>i</sub> − T<sub>ref</sub>)</p>

where A<sub>i</sub> is 1 for a zone with crops and 0 otherwise, T<sub>i</sub> is the zone temperature, and T<sub>ref</sub> is a reference temperature, initially 29 °C (the control target used in the survey, Section 2.3), the upper end of the crops' preferred range. Summed over time, H gives the crops' heat exposure in degree-minutes.

### 4.2. Technical Requirements

Table 6 lists the technical requirements. Targets marked "proposed" will be finalised from bench data and baseline measurements.

[[table: table-requirements | Table 6: Technical requirements and targets]]

### 4.3. Scope of Work

Table 7 sets out what this project will deliver, alongside the long-term application and stretch goals. Only fans are varied; the greenhouse structure stays fixed. Physical tests use four floor fans in the germination section.

[[table: table-scope | Table 7: Scope of work]]

**Out of scope:** changes to GH1's structure, vents, misting or shading; guaranteeing crop-optimal temperatures at peak sun; air-conditioning; proving yield or profit improvement; and developing weather forecasts (NEA data is used as an input).
