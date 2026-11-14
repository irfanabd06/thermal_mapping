---
title: 6. System Architecture and Detailed Design
---
### 6.1. System Architecture

The system has four subsystems (Figure 12). S1 measures conditions across the crop zones. S2 turns the measurements into a live thermal map and hotspot index (the digital twin) and, separately, runs offline CFD to evaluate fan layouts. S3 decides fan actions from the hotspot index, and S4 carries them out with floor fans, whose effect is then measured again by S1. A local dashboard shows the map, hotspots and fan status. All live processing runs on a Raspberry Pi 5, so the system keeps working without internet access.

![Figure 12. System architecture](assets/fig-system-architecture.png)

### 6.2. S1: Sensor Nodes

Two node types share one design (Figure 13), built around an ESP32-C6 microcontroller. Type A nodes measure air temperature and humidity with an SHT45 and form the main grid. Type B nodes add an MLX90640 thermal camera (32 × 24 pixels) aimed at the canopy to estimate leaf temperature, and are placed at fewer locations. The firmware takes the median of 10 SHT45 readings and averages 10 thermal frames, with emissivity set to 0.95, to reduce noise.

![Figure 13. Sensor-node functional blocks and schematic](assets/fig-sensor-node-design.png)

Because sunlight heats exposed sensors (Section 7.1), the SHT45 sits in a ventilated, louvred shield, separated from the electronics and battery compartment (Figure 14). Making the enclosure smaller and choosing the power supply are Semester 2 tasks.

![Figure 14. Open sensor (left) and the ventilated, shielded enclosure concept (right)](assets/fig-sensor-enclosure.jpg)

### 6.3. S1: Communication and Edge Gateway

Nodes send JSON packets containing a node ID, sequence number and readings over RS-485 (9600 baud, 8N1) to a USB–RS-485 adapter on the Raspberry Pi 5 (Figure 15). On the Pi, Docker runs a Mosquitto MQTT broker and Node-RED, which time-stamp, process and store the data, with InfluxDB planned for time-series storage. Multi-node addressing and fault handling are still to be implemented.

![Figure 15. Edge gateway and data pipeline](assets/fig-edge-gateway.png)

### 6.4. S2: Thermal Map, CFD Model and Digital Twin

The live thermal map interpolates node readings across the crop zones using a Gaussian process, which also estimates the uncertainty between nodes. The 57-point survey will be used to choose node spacing: a layout is acceptable if it finds the same crop-zone hotspots as a dense survey (R5).

The CFD model of GH1 is built in SOLIDWORKS Flow Simulation. To keep it tractable, the measured roof surface temperature replaces a full solar-radiation model, crops are modelled as a porous zone, and existing fans use their rated airflow. The model is calibrated on one day and checked against another for trend agreement (R6). A Grafana dashboard on the Pi shows the map, hotspot index and fan status.

### 6.5. S3 and S4: Control and Actuation

The controller uses simple, transparent rules rather than predictive control. When a crop zone's exceedance H rises above a threshold, the fans that most influence that zone, identified from fan step tests and CFD, are switched on or sped up. When H falls back, they return to low speed or off. A minimum on/off time prevents rapid cycling, and if sensors or the controller fail, the fans revert to baseline operation (on).

S4 uses floor circulation fans procured for the project, ideally low-voltage DC fans with PWM speed control, so the farm's mains wiring is not changed. Fan energy is metered to evaluate the cost side of the trade-off.
