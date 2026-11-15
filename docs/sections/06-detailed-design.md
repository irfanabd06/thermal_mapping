---
title: 6. System Architecture and Detailed Design
---
### 6.1. System Architecture

The system has three subsystems, one for each objective (Figure 13). S1 serves both applications, and the four floor fans are shared: S2 uses them to test layouts and S3 to control cooling. All live processing runs on a Raspberry Pi 5, so the system keeps working without internet access.

- **S1 Sense and Map:** samples temperature, humidity and canopy temperature across the crop zones every 30 minutes, using permanent nodes and, during training, temporary ones. It cleans the data and estimates conditions between nodes with soft sensors and Gaussian process regression.
- **S2 Cooling Layout Evaluation (Application 1, before the greenhouse is built or retrofitted):** the CFD flow model, using measured inputs from S1, is used to choose the best fan layout before fans are installed. Its suggested layouts are checked by building them with the floor fans and measuring the temperature improvement.
- **S3 Live Cooling Control (Application 2, once the greenhouse is operating):** running on the chosen layout, it predicts crop-zone hotspots 30 minutes ahead, supported by NEA weather data when online, then switches on the floor fans that most affect them and shows the results on a dashboard. S1 measures the effect.

![Figure 13. System architecture: three subsystems, with the two applications as S2 and S3](assets/fig-system-architecture.png)

### 6.2. Subsystem Goals

Table 8 defines what each subsystem must deliver and how it will be verified. Each subsystem matches one requirement group in Table 7.

[[table: table-subsystems | Table 8: Subsystem goals, deliverables and verification]]

### 6.3. S1: Sense and Map

**Plant Stress Indicator: Leaf Vapour Pressure Deficit**

Besides temperature and humidity, S1 reports two indicators of crop stress. Vapour pressure deficit (VPD) is how much more moisture the air could hold, which drives transpiration. Leaf VPD (LVPD) uses the leaf temperature from the Type B nodes in place of air temperature, so it shows what the plant itself experiences (Appendix C).

<p class="equation">e<sub>s</sub>(T) = 0.6108 · exp(17.27 T / (T + 237.3)) kPa</p>

<p class="equation">VPD = e<sub>s</sub>(T<sub>air</sub>) · (1 − RH/100)</p>

<p class="equation">LVPD = e<sub>s</sub>(T<sub>leaf</sub>) − e<sub>s</sub>(T<sub>air</sub>) · RH/100</p>

#### 6.3.1. Detailed Design

Table 9 sets out the S1 design. Both node types share one ESP32-C6 design (Appendix F), and data flows to the edge gateway on the Raspberry Pi 5 (Figure 14).

[[table: table-s1-design | Table 9: S1 detailed design]]

![Figure 14. Raspberry Pi Edge gateway and data pipeline](assets/fig-edge-gateway.png)

#### 6.3.2. Initial Prototype

One prototype node was built in Semester 1, with an SHT45, an MLX90640 and an RS-485 link to the Raspberry Pi 5. Because sunlight heats exposed sensors (Section 6.3.3), both node types use the same 3D-printed enclosure: a ventilated, louvred shield for the SHT45, mounted above a closed electronics compartment (Figure 15).

- **Type A:** fully shielded. The initial prototype (Figure 15a) is this type.
- **Type B:** the same enclosure, with an opening for the MLX90640 to view the leaves.

Making the enclosure smaller and choosing the power supply are Semester 2 tasks.

![Figure 15. Sensor-node enclosure: (a) initial prototype, (b) Type A design, (c) Type B design with an opening for the MLX90640](assets/fig-sensor-enclosure.png)

#### 6.3.3. Testing and Analysis

Semester 1 testing checked whether the sensing chain produces trustworthy data. Each test states its purpose, method, result and analysis against the requirements in Table 7.

**<u>SHT45 air temperature and humidity</u>**

- **Purpose:** check that the SHT45 agrees with a reference closely enough for baseline comparisons (R1).
- **Method:** the open (unshielded) SHT45 was logged side by side with a Kestrel 5000 weather meter, first on the bench for about 10 minutes, including a heating step, and then in GH1 for about 30 minutes (Figure 16).
- **Result:** on the bench, the SHT45 agreed with the reference to 0.33 °C and 2.35 %RH (RMSE), meeting R1. In the greenhouse, it read 4.3 °C higher and 10 %RH lower than the reference (Table 10), a bias consistent with direct solar heating of the sensor.
- **Analysis:** the 4.0 °C spread in the survey is about 12 times the SHT45's bench error (0.33 °C RMSE), so a grid of these sensors can resolve the spatial differences that matter, provided the sensors are shielded. The pattern of warm main plant zones and cooler germination and seedling zones supports the claim that one monitoring point is not representative. However, if the survey points were measured one after another, the spread also includes change over time, so the result is treated as indicative until it is repeated with simultaneous loggers. Clouds and misting also change conditions within minutes, as the sharp steps in Figure 16 show. This supports evaluating solutions against a baseline measured under comparable conditions, rather than against absolute temperature targets.

![Figure 16. SHT45 compared with a Kestrel 5000 on the bench (top) and in GH1 (bottom)](assets/fig-sht45-validation.png)

[[table: table-sht45 | Table 10: SHT45 agreement with the Kestrel 5000 reference]]

> TODO: Add the date and time of both tests.

**<u>Sensor enclosure</u>**

- **Purpose:** reduce the solar bias found in the SHT45 test (R2).
- **Method:** the SHT45 inside the ventilated, louvred shield (Figure 15) was compared with the reference in GH1 over three paired readings.
- **Result:** the shielded sensor read 0.8–2.1 °C above the reference, a mean bias of +1.6 °C. This is about 2.7 °C (63%) lower than the open sensor's +4.3 °C, but still above the 0.5 °C target, so R2 is not yet met.
- **Analysis:** the unshielded bias (+4.3 °C) is as large as the spatial spread itself, so without shielding, sensor heating would be indistinguishable from real hotspots. The enclosure improved the measurement by about 2.7 °C, cutting the bias to +1.6 °C. This rests on only three readings, so it is indicative, and the remaining bias is still above the R2 target. Improving the shield is therefore the first Semester 2 priority. The next tests will log the shielded and open sensors side by side over a full day, and check the enclosure's resistance to wear in high humidity and misting (R3).

**<u>MLX90640 canopy temperature</u>**

- **Purpose:** check that the low-cost thermal camera gives usable canopy temperatures.
- **Method:** MLX90640 frames of the same plant were compared with a handheld thermal camera at distances of 50–500 mm (Figure 17).
- **Result:** centre temperatures agreed within 1.3 °C, but maximum temperatures were 1.8–3.8 °C lower (Table 11), because each MLX90640 pixel averages over a larger area.
- **Analysis:** the MLX90640 tracks the centre temperature of the reference camera but underestimates peak surface temperatures. It will therefore be used for zone-average canopy temperature rather than detecting small hot spots.

![Figure 17. MLX90640 frames (left of each pair) compared with a handheld thermal camera at 50–500 mm](assets/fig-mlx90640-check.jpg)

[[table: table-mlx | Table 11: MLX90640 compared with a handheld thermal camera]]

### 6.4. S2: Cooling Layout Evaluation

#### 6.4.1. Detailed Design

The CFD model of GH1 is built in SOLIDWORKS Flow Simulation from measured inputs (Table 12). Because conditions change quickly, it is judged on trends and rankings rather than absolute temperatures.

[[table: table-s2-design | Table 12: S2 detailed design]]

#### 6.4.2. Initial Prototype

In Semester 1, GH1's geometry and existing fans were measured (Appendices D and E) and the existing airflow was mapped (Section 2.4). The test-section model will be built first, in Semester 2.

#### 6.4.3. Testing and Analysis

Planned for Semester 2. The baseline model will first be checked against the measured temperature pattern. The top suggested layouts will then be built with the floor fans, and their measured improvement compared with the predicted ranking (R7, R8).

### 6.5. S3: Live Cooling Control

#### 6.5.1. Detailed Design

S3 runs on the Raspberry Pi 5 with the chosen fan layout and uses simple, transparent rules (Table 13).

[[table: table-s3-design | Table 13: S3 detailed design]]

#### 6.5.2. Initial Prototype

None yet. The floor fans will be procured, and their speed control and power interface chosen, at the start of Semester 2.

#### 6.5.3. Testing and Analysis

Planned for Semester 2: predicted against measured exceedance over test days (R9), logged predictions against fan commands with a fault-injection test (R12), and alternating-day trials of baseline against control for exceedance and fan energy (R10, R11).
