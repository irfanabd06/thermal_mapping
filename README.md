# [CDE4301] IS-405: Thermal Mapping & Greenhouse Environmental Control

Final Year Project | National University of Singapore

Development of a sensor-informed greenhouse digital twin integrating distributed environmental sensing, thermal simulation, edge computing and model-informed environmental control.

---

## Project Report

**[View the CDE4301 Project Report](https://irfanabd06.github.io/thermal_mapping/)**

The report is hosted using GitHub Pages and documents the project's background, methodology, engineering design, prototype development, experimental results and evaluation.

**[View Report Source Files](docs/)**

> Note: The report website must be enabled under GitHub Pages before the published link becomes accessible.

---

## Thermal Map Dashboard

**[Open the Greenhouse 1 Thermal Map](https://irfanabd06.github.io/thermal_mapping/dashboard/)**

An interactive 3D model of Greenhouse 1 with the preliminary 57-point survey shown as a heat map at 1 m height, hot zones against the 29 °C target, fan positions, and site weather. It is served from [`docs/dashboard/`](docs/dashboard/) by the same GitHub Pages site as the report.

- Source and build instructions: [`dashboard/`](dashboard/)
- Greenhouse CAD model: [`cad/Greenhouse1.step`](cad/Greenhouse1.step)

---

## Project Overview

Tropical greenhouses experience spatially non-uniform thermal conditions due to solar radiation, ventilation patterns, greenhouse geometry and cooling configurations.

This project aims to develop a digital twin-based environmental control system that characterises greenhouse microclimates, evaluates cooling strategies and supports spatially informed environmental control.

### Project Objectives

1. **Spatial Environmental Monitoring** — Characterise greenhouse thermal distributions using distributed sensing.
2. **Thermal Modelling & Cooling Evaluation** — Model spatial thermal conditions and evaluate cooling configurations through simulation.
3. **Environmental Control** — Develop and evaluate control strategies to improve thermal uniformity and cooling effectiveness.

## System Architecture

The proposed solution consists of four subsystems:

| Subsystem | Description |
|---|---|
| **01 — Sensing & Data Acquisition** | Distributed ESP32-C6 sensor nodes, environmental measurements, RS-485 communication and Raspberry Pi 5 edge gateway. |
| **02 — Digital Twin & Simulation** | Thermal mapping, SOLIDWORKS Flow Simulation, MATLAB modelling and 3D visualisation. |
| **03 — Control & Decision-Making** | Spatial environmental analysis and model-informed fan-control algorithms. |
| **04 — Actuation** | Floor-mounted circulation fans for airflow regulation and environmental feedback. |

### Data Acquisition Pipeline

`ESP32-C6 → RS-485 → Raspberry Pi 5 → MQTT → Data Processing & Storage`

The digital twin and control architecture will build upon this data acquisition pipeline.

## Hardware & Software

| Category | Technologies |
|---|---|
| Microcontroller | ESP32-C6 |
| Environmental Sensors | SHT45, MLX90640-BAB |
| Communication | RS-485; Modbus RTU and wireless alternatives under evaluation |
| Edge Gateway | Raspberry Pi 5 |
| Messaging & Orchestration | Mosquitto MQTT, Node-RED |
| Data Storage | SQLite / InfluxDB (under development) |
| CAD & CFD | SOLIDWORKS, SOLIDWORKS Flow Simulation |
| Modelling & Control | Python, MATLAB / Simulink |
| Visualisation | Grafana, Three.js (proposed) |
| Cloud Management | FlowFuse (proposed) |

## Repository Structure

```text
thermal_mapping/
├── cad/                     # Greenhouse 1 STEP model (generated)
├── dashboard/               # Thermal map dashboard source and build scripts
├── docs/                    # CDE4301 report website
│   ├── index.html
│   ├── index.css
│   ├── report-tables.js
│   ├── assets/
│   ├── components/
│   └── dashboard/           # Published dashboard page (generated)
├── experiments/             # Sensor and communication experiments
├── firmware/
│   └── sensor_node/         # ESP32-C6 sensor-node firmware
├── gateway/                 # Raspberry Pi edge gateway
├── requirements.txt
└── README.md
```

## Development Progress

| Workstream | Status |
|---|---|
| Greenhouse site investigation | Completed |
| Preliminary 57-point thermal survey | Completed |
| SHT45 and MLX90640 sensor acquisition | Prototype tested |
| RS-485 sensor-to-gateway communication | Prototype tested |
| MQTT telemetry | Prototype tested |
| Edge data storage | In development |
| Digital twin and CFD simulation | In development |
| Environmental control and actuation | Planned |

## Report Website Development

The CDE4301 report is a static website based on the iDP report template, maintained in [`docs/`](docs/).

### Publishing

To publish the report using GitHub Pages:

1. Open the GitHub repository.
2. Navigate to **Settings → Pages**.
3. Under **Build and deployment**, select **Deploy from a branch**.
4. Select branch `main` and folder `/docs`.
5. Save the settings.

The website should become available at:

https://irfanabd06.github.io/thermal_mapping/

### Editing the Report

The report text lives in Markdown files, one per section, in [`docs/sections/`](docs/sections/). `docs/index.html` loads them automatically, so there is no need to edit HTML.

| Task | Location |
|---|---|
| Report text | `docs/sections/*.md` |
| Section order | `docs/sections/sections.json` |
| Report tables | `docs/report-tables.js` |
| Images and figures | `docs/assets/` |
| Website styling | `docs/index.css` |
| Reusable website components | `docs/components/` |

**Visual editor:** the repo includes a [Pages CMS](https://pagescms.org) configuration (`.pages.yml`). Sign in at [app.pagescms.org](https://app.pagescms.org) with GitHub and open this repo to edit sections in a rich-text editor; each save is a commit.

Inside a section file:

| To add | Write |
|---|---|
| A table from `report-tables.js` | `[[table: table-requirements \| Table 3: Technical requirements and targets]]` |
| A captioned figure | `![Figure 1: GH1 layout](assets/gh1-layout.png)` on its own line |
| A draft note (not counted) | `> TODO: what still needs writing` |

**Local preview:** the page loads the section files over HTTP, so opening `index.html` directly will not work. Run `python3 -m http.server` inside `docs/` and open http://localhost:8000.

### Word Count

Count the words in the report sections (TODO notes, tables, references and appendices are excluded):

```bash
python3 tools/wordcount.py
```

The report template specifies a 3,000-word limit, excluding appendices and references. Verify the applicable submission requirements before finalising the report.

## Firmware Dependencies

The ESP32-C6 firmware uses the official Melexis MLX90640 library as a Git submodule.

Clone the repository with submodules:

```bash
git clone --recurse-submodules https://github.com/irfanabd06/thermal_mapping.git
```

For an existing clone:

```bash
git submodule update --init --recursive
```

---

**CDE4301 — Thermal Mapping & Greenhouse Environmental Control**
