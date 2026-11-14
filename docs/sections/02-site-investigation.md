---
title: 2. Site Investigation and Problem Analysis
---
### 2.1. Greenhouse 1

**Site: ComCrop rooftop farm, 15 Woodlands Loop**

This project uses Greenhouse 1 (GH1) at ComCrop as its reference greenhouse for studying tropical greenhouse thermal management. Site visits were conducted to document its geometry, growing zones, cooling infrastructure and operational conditions.

The growing zones and fan positions are shown in Figure 2.

![Figure 2. GH1 layout showing the growing zones and fan positions](assets/fig-gh1-layout.png)

[[table: table-gh1 | Table 1: GH1 site parameters]]

![Figure 3. Interior of Greenhouse 1 (GH1) at ComCrop, showing the hydroponic growing channels, retractable shade nets and circulation fans](assets/fig2-gh1-interior.jpg)

### 2.2. Existing Cooling and Operating Conditions

GH1's existing cooling equipment is summarised in Table 2.

[[table: table-gh1-operation | Table 2: GH1 cooling equipment and operating conditions]]

### 2.3. Spatial Thermal Survey

Preliminary measurements were taken on a sunny day, 31 °C, avoiding cooler or hazy weather. Shading was deployed to cover most of the GH1's roof area. Measuring instruments used:

- UTi260B, Professional thermal Imager: Surface Temperature
- Kestrel 5000 Environmental Meter: Ambient Temperature and Relative Humidity

A capture of the interior of GH1 showed larger surface-temperature differences: 47.3 °C at the roof, 34.7 °C at the plants and 32.2 °C at the roof near the misting line (Figure 4). These are surface rather than air temperatures, but they indicate heat accumulating under the roof.

![Figure 4. Thermal images of GH1: roof, plant and misting-line surface temperatures, taken at 10.51 am](assets/fig-gh1-thermal-images.jpg)

To test whether a single monitoring point is representative, air temperature was measured at 57 points across GH1 at 1 m height, close to canopy level (Figure 5, Table 3). Readings ranged from 35.5 °C to 39.5 °C, a spread of 4.0 °C.

![Figure 5. Air temperature at 1 m height from the 57-point survey, with fan positions and airflow directions](assets/fig-thermal-survey-heatmap.png)

**Measurement grid.** 57 points at 1 m height. Spacing on site was 3 to 3.5 m. The model places point T(3k + r) at s = 1.5 + 3.1k m (k = 0 to 18) and t = 3.0 + 3.25(r − 1) m (r = 1 to 3), so a point may be up to about 0.5 m from where it was taken.

[[table: table-survey | Table 3: Preliminary survey (°C, time not recorded)]]

**Summary:** mean 38.03 °C, which is 9.0 °C over the 29 °C target. Hottest T53 at 39.5 °C, coolest T14 at 35.5 °C. Main section (T1 to T36) mean 37.45 °C, wing (T40 to T57) mean 39.03 °C.

> TODO: Add the survey time, fan states, and whether the 57 points were measured one after another or at the same time.

### 2.4. Problem Analysis

The site findings point to one underlying problem: decisions about GH1's cooling are made without spatially resolved thermal information. This affects two stages (Figure 6). At the design stage, the number and placement of fans were chosen without evaluating how air and heat move through the greenhouse, and testing alternatives physically is slow and costly. At the operation stage, a single sensor cannot show where crops are hottest, so fans run continuously regardless of local conditions. This project therefore treats the lack of useful thermal data, rather than a lack of cooling equipment, as the root cause to address.

![Figure 6. Root cause, affected stages and the two applications of the proposed solution](assets/fig-problem-framing.png)
