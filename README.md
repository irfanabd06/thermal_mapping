# CDE4301 Thermal Mapping of Greenhouse

Final Year Project for CDE4301.

## Project Overview

This project develops a distributed sensing and control system for thermal mapping and environmental monitoring of a greenhouse.

The system will include:

- Distributed environmental sensor nodes
- ESP32-based sensor acquisition
- Communication between sensor nodes and gateway
- Raspberry Pi gateway
- Edge computing and local control
- Database and data storage
- Cloud backend
- Web dashboard and thermal mapping
- Remote control
- Greenhouse actuator control

## System Architecture

Development in progress.

## Report Website

The CDE4301 report is a static site in [`docs/`](docs/), based on the iDP report template.

- **Publish:** GitHub → Settings → Pages → Source: *Deploy from a branch* → Branch `main`, folder `/docs`.
  The site is then served at `https://irfanabd06.github.io/thermal_mapping/`.
- **Edit text:** `docs/index.html`. Draft placeholders are `<sl-alert class="todo">` blocks; delete each one once its section is written.
- **Edit tables:** `docs/report-tables.js`.
- **Images:** put them in `docs/assets/` and use `<image-component source="assets/..." subtitle="Figure N: ...">`.
- **Word count:** `python3 tools/wordcount.py` counts the report body against the 3,000-word limit (appendices and references excluded).