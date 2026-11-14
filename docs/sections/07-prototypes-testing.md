---
title: 7. Prototypes and Testing
---
Semester 1 testing focused on whether the sensing chain produces trustworthy data. Each test states its purpose, method and result against the requirements in Table 6.

### 7.1. SHT45 Air Temperature and Humidity

- **Purpose:** check that the SHT45 agrees with a reference closely enough for baseline comparisons (R1).
- **Method:** the SHT45 was logged side by side with a Kestrel 5000 weather meter, first on the bench for about 10 minutes, including a heating step, and then in GH1 for about 30 minutes (Figure 15).
- **Result:** on the bench, the SHT45 agreed with the reference to 0.33 °C and 2.35 %RH (RMSE), meeting R1. In the greenhouse, it read 4.3 °C higher and 10 %RH lower than the reference (Table 10), a bias consistent with direct solar heating of the sensor.

![Figure 15. SHT45 compared with a Kestrel 5000 on the bench (top) and in GH1 (bottom)](assets/fig-sht45-validation.png)

[[table: table-sht45 | Table 10: SHT45 agreement with the Kestrel 5000 reference]]

> TODO: Confirm whether the greenhouse test used the open sensor, and the date and time of both tests.

### 7.2. Sensor Enclosure

- **Purpose:** reduce the solar bias found in Section 7.1 (R2).
- **Method:** the SHT45 was compared open and inside the ventilated, louvred shield (Figure 13) against the reference.
- **Result:** readings were closer to the reference in the shielded enclosure. The remaining bias has not yet been quantified, so R2 is not yet verified.

> TODO: Add the measured bias for the shielded sensor, if recorded.

### 7.3. MLX90640 Canopy Temperature

- **Purpose:** check that the low-cost thermal camera gives usable canopy temperatures.
- **Method:** MLX90640 frames of the same plant were compared with a handheld thermal camera at distances of 50–500 mm (Figure 16).
- **Result:** centre temperatures agreed within 1.3 °C, but maximum temperatures were 1.8–3.8 °C lower (Table 11), because each MLX90640 pixel averages over a larger area.

![Figure 16. MLX90640 frames (left of each pair) compared with a handheld thermal camera at 50–500 mm](assets/fig-mlx90640-check.jpg)

[[table: table-mlx | Table 11: MLX90640 compared with a handheld thermal camera]]

### 7.4. RS-485 and MQTT Telemetry

- **Purpose:** verify the data path from node to gateway (R4).
- **Method:** an ESP32-C6 node sent packets over RS-485 to the Raspberry Pi 5, which published them through Mosquitto.
- **Result:** complete JSON packets, including all 768 thermal pixels, the node ID and sequence numbers, were received consecutively and published over MQTT. Packet-delivery rate and latency over a long run have not yet been measured.
