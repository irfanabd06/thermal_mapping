---
title: 5. Design Specifications
---
### 5.1. Baseline-Referenced Validation

This project focuses on comparative evaluation rather than reaching optimal conditions. Results depend on the weather: on very hot days, crop temperatures cannot be brought down to the optimal range, and passing clouds, wind and misting disturb every measurement. Each solution is therefore compared against a reference baseline: GH1's current operation, with existing fans running continuously, measured under comparable weather. The requirements ensure that measurement error is small enough for those comparisons to be meaningful.

Hotspots are judged only where crops grow, using a crop-zone exceedance index for each zone *i*:

<p class="equation">H<sub>i</sub> = A<sub>i</sub> · max(0, T<sub>i</sub> − T<sub>ref</sub>)</p>

where A<sub>i</sub> is 1 for a zone with crops and 0 otherwise, T<sub>i</sub> is the zone temperature, and T<sub>ref</sub> is a reference temperature, initially 29 °C, the upper end of the crops' preferred range. Summed over time, H gives the crops' heat exposure in degree-minutes.

### 5.2. Technical Requirements

Table 7 lists the technical requirements. Targets marked "proposed" will be finalised from bench data and baseline measurements.

[[table: table-requirements | Table 7: Technical requirements and targets]]
