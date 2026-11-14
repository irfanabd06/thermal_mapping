// Data for the report's Grid.js tables.
// Edit the arrays here. Place a table in a section file with: [[table: <id> | <caption>]]

const tables = {
  // Table 1: GH1 site parameters (Section 2.1)
  "table-gh1": {
    columns: ["Parameter", "Value"],
    data: [
      ["Length", "~57 m"],
      ["Width", "12.5 m"],
      ["Floor area", "~712.5 m²"],
      ["Wall height", "~3 m"],
      ["Roof peak height", "~4.35 m"],
      ["Roof type", "Gable-capped monitor"],
      ["Side walls", "Insect netting on both long sides"],
      ["Crops", "Lettuce, kai lan, bak choi, basil and others"],
    ],
  },

  // Table 2: GH1 cooling equipment and operating conditions (Section 2.2)
  "table-gh1-operation": {
    columns: ["Item", "Details"],
    data: [
      ["Ventilation fans", "4, running 24/7"],
      ["Ceiling circulation fans", "6, running 24/7"],
      ["Floor circulation fans", "Installed, not in use"],
      ["Misting", "Operates throughout the day"],
      ["Shading", "Retractable shade nets"],
      ["Monitoring", "Single point: weather station and monitoring dashboard"],
      ["Reported peak temperature", "45 °C (operator-reported)"],
      ["Preferred crop conditions", "24–30 °C, 60–80% RH"],
      ["Current use", "Reported unsuitable for commercial production; now leased by NUS for research and student experimentation"],
    ],
  },

  // Table 3: Problem → solution map (Section 3.3)
  "table-problem-solution": {
    columns: ["Target problem (evidence)", "Solution", "Objective", "Requirements"],
    data: [
      [
        "P1. Insufficient spatial data: one monitoring point, yet a 4.0 °C spread across 57 points",
        "Durable sensor grid and crop-height thermal map",
        "O1 Thermal characterisation",
        "R1–R5",
      ],
      [
        "P2. Fan layout chosen without thermal analysis; physical trials are slow and costly",
        "CFD baseline of GH1 and comparison of fan configurations",
        "O2 Modelling and design evaluation",
        "R6–R7",
      ],
      [
        "P3. Fans run 24/7 without spatial or timing logic; high running cost",
        "Digital twin with crop-zone hotspot control of floor fans and a dashboard",
        "O3 Digital twin and control",
        "R8–R13",
      ],
    ],
  },

  // Table 4: Scope of work (Section 3.4)
  "table-scope": {
    columns: ["Area", "Long-term application", "CDE4301 deliverable (committed)", "Stretch goal"],
    data: [
      ["Sensing", "Adaptable sensing for any greenhouse", "Sensor grid in a GH1 test section, durability-tested", "Wireless option (Zigbee or Wi-Fi) benchmarked"],
      ["Thermal map", "Real-time 3D microclimate", "2D crop-height thermal map with uncertainty", "3D view (Three.js)"],
      ["Design evaluation", "Optimise greenhouse designs before construction", "CFD baseline of GH1 and ≥ 10 fan configurations compared", "Surrogate model and automated search"],
      ["Control", "Adaptive, predictive greenhouse management", "Rule-based crop-zone hotspot control of floor fans, tested against baseline", "Forecast-based scheduling"],
      ["Dashboard", "Farm-wide management interface", "Local dashboard: map, hotspots, fan status, energy", "Remote access"],
      ["Commercial value", "Higher profit and better crops", "Fan energy vs hotspot trade-off measured", "Yield and quality trials (future work)"],
    ],
  },

  // Table 5: Constraints (Section 3.5)
  "table-constraints": {
    columns: ["Constraint", "Description", "Design implication"],
    data: [
      ["Physical", "Existing GH1 geometry and crop zones; no structural changes", "Nodes mounted on benches and frame; CFD varies fans only"],
      ["Environmental", "Up to 45 °C, high humidity, daily misting, direct sun", "Shielded, ventilated enclosures; humidity-resistant electronics"],
      ["Connectivity", "Limited network infrastructure on site", "Local-first processing on the edge gateway; wired RS-485 backbone"],
      ["Power", "Nodes spread far from power outlets", "Low-power nodes; supply architecture to be decided"],
      ["Operational", "Minimal disruption to cultivation; existing equipment untouched", "Actuation limited to the project's own floor fans"],
      ["Cost", "Student budget; farmers are cost-sensitive", "Low-cost sensors; each sensor justified; per-node cost target"],
      ["Safety", "Work alongside staff, water and mains equipment", "Low-voltage fans or certified switching; fail-safe control"],
    ],
  },

  // Table 6: Technical requirements and targets (Section 4.2)
  "table-requirements": {
    columns: ["ID", "Requirement", "Target", "Rationale", "Verification", "Status"],
    data: [
      ["R1", "Sensor agreement with reference", "≤ 0.5 °C and ≤ 3 %RH RMSE", "Error must be well below the 4 °C spread being mapped", "Side by side with Kestrel 5000", "Bench met (0.33 °C, 2.35 %RH)"],
      ["R2", "Radiation-shield bias", "≤ 0.5 °C mean bias in daytime GH1 (proposed)", "Unshielded bias was +4.3 °C, as large as the spread", "Shielded node vs reference in sun", "Not met unshielded; shielded to quantify"],
      ["R3", "Durability in humidity", "≥ 14 days in GH1 with misting; ≥ 95% valid readings; electronics compartment ≥ IP54", "High night-time RH and daily misting", "Field deployment log", "Not tested"],
      ["R4", "Data delivery", "≥ 99% packets (wired) over 7 days; latency ≤ 5 s; sampling ≤ 60 s", "Gaps break the map and the controller", "Sequence-number counts", "Short bench run passed"],
      ["R5", "Hotspot detection", "Layout finds the hottest crop zone identified by a dense survey in ≥ 80% of test periods (proposed)", "Sets node spacing without over-instrumenting", "Sparse vs dense layout comparison", "Not tested"],
      ["R6", "Model trend agreement", "CFD ranks crop zones and fan effects in the same order as measurements", "Design advice depends on ranking, not absolute values", "Measured vs simulated; fan step tests", "Not started"],
      ["R7", "Configuration study", "≥ 10 fan configurations compared with baseline", "Enough to show trends and a best option", "CFD runs", "Not started"],
      ["R8", "Dashboard update", "Map, hotspots and fan states refreshed ≤ 1 min, locally", "Operators need current information", "Timed test on the Pi", "Not started"],
      ["R9", "Hotspot reduction", "Crop-zone exceedance (°C·min above 30 °C) ≥ 20% lower than baseline (proposed)", "Primary measure of thermal benefit", "Alternating-day trials, weather-normalised", "Not started"],
      ["R10", "Energy trade-off", "Fan energy ≤ baseline for equal or better exceedance", "Cost side of the farmer's balance", "Fan energy metering", "Not started"],
      ["R11", "Safe control", "Fans revert to baseline on fault; minimum on/off time ≥ 10 min", "Crop safety and equipment wear", "Fault-injection test", "Not started"],
      ["R12", "Electrical safety", "Fans ≤ 24 V DC or certified switching; farm mains untouched", "Safe, reversible installation", "Design review", "Not started"],
      ["R13", "Local-first operation", "Runs without internet; auto-restart ≤ 5 min after power loss", "Limited connectivity on site", "Network-unplug and power-cycle tests", "Not tested"],
    ],
  },

  // Table 7: Subsystem goals (Section 4.3)
  "table-subsystems": {
    columns: ["Subsystem", "Goal", "Deliverables", "Verified by", "Status (end of Semester 1)"],
    data: [
      ["S1 Sense", "Durable, location-tagged crop-zone T/RH and canopy temperature", "Type A/B nodes, shielded enclosure, RS-485 network, gateway logging", "R1–R5", "Prototype node; bench accuracy tested; RS-485 to MQTT verified"],
      ["S2 Map & Model", "Live thermal map and hotspot index; validated CFD baseline; fan-configuration comparison", "Gaussian-process map, CFD model, configuration ranking, dashboard", "R5–R8", "57-point survey and heatmap; GH1 dimensions recorded"],
      ["S3 Decide", "Decide fan actions from crop-zone hotspots", "Hotspot index; rule-based controller with fail-safe", "R9, R11, R13", "Control approach defined"],
      ["S4 Actuate", "Run fan commands safely and measure their energy", "Procured floor fans, speed/relay interface, energy metering", "R9–R12", "Fans to be procured"],
    ],
  },

  // Table 8: Concept selection (Section 5.2)
  "table-concepts": {
    columns: ["Decision", "Options considered", "Selected", "Reason"],
    data: [
      ["Sensor-to-gateway link", "RS-485, Wi-Fi, BLE, Zigbee, LoRa", "RS-485; one wireless option benchmarked", "Robust over ~57 m and already verified end to end; wireless avoids cabling but needs reliability and power testing"],
      ["Actuation", "Modify ventilation or misting; control existing fans; procure own floor fans", "Procured floor circulation fans", "Existing systems cannot be modified; own fans are safe, movable and allow speed tests"],
      ["Modelling approach", "Run CFD live; data-only interpolation; offline CFD plus sensor-updated map", "Offline CFD plus sensor-updated map", "CFD is too slow for live control; data alone cannot evaluate untested fan layouts"],
      ["Thermal map method", "Inverse-distance weighting; Gaussian process; CFD-based", "Gaussian process", "Also estimates uncertainty, showing where more sensors are needed"],
      ["CFD tool", "SOLIDWORKS Flow Simulation; ANSYS Fluent; OpenFOAM", "SOLIDWORKS Flow Simulation", "Integrated with the CAD model and available; adequate for comparative studies"],
      ["Edge computer", "Raspberry Pi 5; laptop; cloud", "Raspberry Pi 5", "Low cost and power; runs Docker, MQTT and Node-RED locally"],
      ["Controller", "PID; rule-based; model predictive control", "Rule-based (MPC as stretch)", "Transparent and testable in the timeline; disturbances limit the benefit of precise control"],
    ],
  },

  // Table 9: CFD study scope (Section 5.3)
  "table-sim-scope": {
    columns: ["Parameter", "Treatment"],
    data: [
      ["Greenhouse geometry, roof, walls and netting", "Fixed (GH1 as built)"],
      ["Existing ventilation and ceiling fans", "Fixed, as baseline operation"],
      ["Number of floor fans", "Variable"],
      ["Fan positions and orientation", "Variable"],
      ["Fan speed", "Variable, within the procured fans' range"],
      ["External weather", "Representative midday, morning and overcast cases"],
      ["Outputs", "Crop-zone temperature, exceedance H, airflow, fan power"],
    ],
  },

  // Table 10: SHT45 vs Kestrel 5000 (Section 7.1)
  "table-sht45": {
    columns: ["Test", "Quantity", "Mean error", "MAE", "RMSE"],
    data: [
      ["Bench (~10 min)", "Temperature", "+0.10 °C", "0.22 °C", "0.33 °C"],
      ["Bench (~10 min)", "Relative humidity", "+0.69 %RH", "1.62 %RH", "2.35 %RH"],
      ["GH1 (~30 min)", "Temperature", "+4.28 °C", "4.28 °C", "4.77 °C"],
      ["GH1 (~30 min)", "Relative humidity", "−10.02 %RH", "10.02 %RH", "10.53 %RH"],
    ],
  },

  // Table 11: MLX90640 vs handheld thermal camera (Section 7.3)
  "table-mlx": {
    columns: ["Distance", "MLX90640 centre", "Reference centre", "Difference", "MLX90640 max", "Reference max"],
    data: [
      ["50 mm", "33.5 °C", "33.8 °C", "−0.3 °C", "35.6 °C", "38.3 °C"],
      ["100 mm", "34.0 °C", "35.3 °C", "−1.3 °C", "38.1 °C", "41.9 °C"],
      ["400 mm", "33.3 °C", "33.3 °C", "0.0 °C", "38.7 °C", "40.5 °C"],
      ["500 mm", "33.3 °C", "32.9 °C", "+0.4 °C", "38.6 °C", "40.8 °C"],
    ],
  },

  // Table 12: Milestones (Section 9.3)
  "table-milestones": {
    columns: ["Milestone", "Date", "Deliverable", "Acceptance criterion"],
    data: [
      ["M1", "31 Dec 2026", "Sensor nodes fabricated with shielded enclosures", "R1 and R2 met on the fabricated nodes"],
      ["M2", "31 Jan 2027", "Sensor grid deployed in the test section; CFD baseline built", "R4 met over 7 days; CFD finds the same hottest crop zone as measurements (R6)"],
      ["M3", "21 Feb 2027", "Fan-configuration study complete", "≥ 10 configurations ranked; top 2–3 selected for physical tests (R7)"],
      ["M4", "14 Mar 2027", "Control loop and dashboard working", "Fans respond to crop-zone hotspots with fail-safe; dashboard live (R8, R11)"],
      ["M5", "11 Apr 2027", "Validation complete", "Baseline vs proposed trials report exceedance and fan energy (R9, R10); durability ≥ 14 days (R3)"],
    ],
  },

  // Table A1: Technology stack (Appendix A)
  "table-stack": {
    columns: ["Function", "Hardware / software", "Status"],
    data: [
      ["Sensor node", "ESP32-C6, SHT45, MLX90640", "Prototype working"],
      ["Node-to-gateway link", "RS-485 (9600 baud, 8N1), USB–RS-485 adapter", "Working"],
      ["Edge gateway", "Raspberry Pi 5, Docker", "Working"],
      ["Messaging", "Mosquitto MQTT", "Working"],
      ["Processing and control", "Node-RED", "Running; flows in progress"],
      ["Storage", "InfluxDB", "Planned"],
      ["CFD", "SOLIDWORKS Flow Simulation", "Planned"],
      ["Modelling and control design", "MATLAB / Simulink", "Planned"],
      ["Dashboard", "Grafana; Three.js (stretch)", "Planned"],
      ["Remote management", "FlowFuse", "Optional"],
    ],
  },

  // Table A2: Firmware parameters (Appendix B)
  "table-firmware": {
    columns: ["Parameter", "Value"],
    data: [
      ["SHT45 aggregation", "Median of 10 readings"],
      ["Thermal aggregation", "Mean of 10 frames"],
      ["Thermal resolution", "32 × 24 (768 pixels)"],
      ["Emissivity setting", "0.95 (assumed for leaves)"],
      ["RS-485 settings", "9600 baud, 8N1"],
      ["Packet contents", "JSON: node ID, sequence number, T/RH, 768-pixel frame; gateway adds timestamp"],
    ],
  },

  // Table A3: Sensor combinations (Appendix C)
  "table-sensor-combos": {
    columns: ["Sensor combination", "Information derived", "Limitation"],
    data: [
      ["Ambient T/RH", "General microclimate", "No leaf-level information"],
      ["Ambient + near-leaf T/RH", "Temperature and humidity gradients", "Cannot isolate contributing factors"],
      ["Ambient T/RH + leaf temperature", "Leaf–air temperature difference, leaf VPD", "Airflow effects unknown"],
      ["Ambient + near-leaf T/RH + leaf temperature", "Local heat and moisture exchange indicators", "Requires calibration or airflow data"],
    ],
  },
};

// Called by report-loader.js once the sections are on the page.
function renderReportTables() {
  for (const [id, config] of Object.entries(tables)) {
    const el = document.getElementById(id);
    if (el && !el.hasChildNodes()) {
      new gridjs.Grid({ ...config, sort: false }).render(el);
    }
  }
}
