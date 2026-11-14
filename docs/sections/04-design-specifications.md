---
title: 4. Design Specifications
---
### 4.1. Baseline-Referenced Validation

Greenhouse measurements are disturbed by passing clouds, wind and misting, so the requirements do not ask for an accurate prediction of temperature. Instead, each solution is compared against a reference baseline: GH1's current operation, with existing fans running continuously, measured under comparable weather. The requirements then ensure that measurement error is small enough for those comparisons to be meaningful.

Hotspots are judged only where crops grow, using a crop-zone exceedance index for each zone *i*:

<p class="equation">H<sub>i</sub> = A<sub>i</sub> · max(0, T<sub>i</sub> − T<sub>ref</sub>)</p>

where A<sub>i</sub> is 1 for a zone with crops and 0 otherwise, T<sub>i</sub> is the zone temperature, and T<sub>ref</sub> is a reference temperature, initially 30 °C, the upper end of the crops' preferred range. Summed over time, H gives the crops' heat exposure in degree-minutes.

### 4.2. Technical Requirements

Table 7 lists the technical requirements. Targets marked "proposed" will be finalised from bench data and baseline measurements.

[[table: table-requirements | Table 7: Technical requirements and targets]]

### 4.3. Subsystem Goals

Table 8 defines what each subsystem must deliver and how it will be verified.

[[table: table-subsystems | Table 8: Subsystem goals, deliverables and verification]]
