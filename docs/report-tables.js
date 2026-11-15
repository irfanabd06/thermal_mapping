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
      ["Crops", "Lettuce, Kai Lan, Bak Choi, Basil, etc"],
    ],
  },

  // Table 2: GH1 cooling equipment and operating conditions (Section 2.2)
  "table-gh1-operation": {
    columns: ["Cooling equipment", "", "Details"],
    data: [
      ["Ventilation fans", { img: "assets/eq-ventilation-fans.jpg" }, "4, running 24/7"],
      ["Ceiling circulation fans", { img: "assets/eq-ceiling-fans.jpg" }, "6, running 24/7"],
      ["Floor circulation fans", { img: "assets/eq-floor-fans.jpg" }, "Installed, not in use"],
      ["Misting", { img: "assets/eq-misting.jpg" }, "Operates throughout the day"],
      ["Shading", { img: "assets/eq-shades.jpg" }, "Retractable shade nets"],
      ["Monitoring", { img: "assets/eq-weather-station.jpg" }, "Single point: weather station and monitoring dashboard"],
    ],
    note:
      "<strong><u>Current Use</u></strong><br>Retired from commercial production. GH1 is now leased by NUS for research and student experimentation<br>Reported peak temperature: 45 °C",
  },

  // Table 4: Problem → solution map (Section 3.3)
  "table-problem-solution": {
    columns: ["Target problem (evidence)", "Objective", "Approach", "Requirements"],
    data: [
      [
        "P1. Uneven thermal conditions",
        "O1 Thermal characterisation",
        "Sensor grid",
        "R1–R6",
      ],
      [
        "P2. Inefficient airflow within greenhouse due to fan layout. Physical trials are slow and costly",
        "O2 Cooling layout evaluation",
        "Flow simulation study",
        "R7–R8",
      ],
      [
        "P3. Fans run without conditional logic, high running cost",
        "O3 Targeted cooling",
        "Hotspot prediction",
        "R9–R14",
      ],
    ],
  },

  // Table 14: Scope of work (Section 7.3)
  "table-scope": {
    columns: ["Area", "Long-term application", "CDE4301 deliverable (committed)", "Stretch goal"],
    data: [
      ["Sensing", "Adaptable sensing for any greenhouse", "Permanent sensor grid plus temporary nodes in the test section (germination section), durability-tested", "Wireless option (Zigbee or Wi-Fi) benchmarked"],
      ["Thermal map", "Real-time 3D microclimate", "2D crop-height map of temperature and humidity, with soft sensors in place of temporary nodes", "3D view (Three.js)"],
      ["Design evaluation", "Optimise greenhouse designs before construction", "Full-GH1 CFD of ≥ 10 fan configurations; tests with 4 floor fans in the test section (number, position, direction, speed)", "Surrogate model and automated search"],
      ["Control", "Adaptive, predictive greenhouse management", "Floor fans switched on from 30-min hotspot predictions, tested against baseline", "Model predictive control"],
      ["Dashboard", "Farm-wide management interface", "Local dashboard: map, hotspots, fan status, energy", "Remote access"],
      ["Commercial value", "Higher profit and better crops", "Fan energy vs hotspot trade-off measured", "Yield and quality trials (future work)"],
    ],
  },

  // Table 5: Constraints (Section 3.4)
  "table-constraints": {
    columns: ["Constraint", "Description", "Design implication"],
    data: [
      { group: "Problem" },
      ["Physical", "Fixed greenhouse structure and crop layout. No structural changes", "Nodes mounted on benches and frame"],
      ["Thermal variability", "Temperature shifts within seconds caused by variable factors", "Sampled measurements have to be cleaned"],
      ["Environmental", "Up to 45 °C, high humidity, daily misting, direct sun", "Shielded, ventilated enclosures and humidity-resistant electronics"],
      ["Cost", "Farmers are cost-sensitive; cooling must not cost more than the crop is worth", "Low-cost sensors; temporary nodes reused across locations"],
      { group: "Project" },
      ["Operational", "Minimal disruption to cultivation. Existing equipment untouched", "Only the project's own floor fans are controlled; physical tests confined to a section of GH1"],
      ["Model uncertainty", "Changing, partly unknown boundary conditions (sun, wind through netting); steady-state CFD cannot follow minute-scale changes", "Evaluations judged on trends and rankings (R7), not absolute temperatures; run for representative weather cases"],
      ["Sensor bias in sun", "Low-cost sensors read high in direct sunlight", "Radiation shield required and its bias verified (R2)"],
      ["Connectivity", "Farms in rural areas may have limited or no internet access", "All live processing on a local edge computer; prediction runs on sensor data alone when offline (R14)"],
      ["Time and season", "Field testing runs January to March 2027, which may not include the hottest conditions", "Weather conditions recorded with every trial; results compared like-for-like with the baseline"],
    ],
  },

  // Table 7: Technical requirements and targets (Section 5.2)
  "table-requirements": {
    columns: ["ID", "Requirement", "Target", "Rationale", "Verification"],
    data: [
      { group: "O1 Thermal characterisation" },
      ["R1", "Sensor agreement", "Co-located nodes agree within 0.5 °C and 5 %RH; each node within 1.0 °C and 5 %RH (RMSE) of reference", "Hotspot detection depends more on nodes agreeing with each other than on absolute accuracy; both well below the 4 °C spread", "Nodes co-located with each other and a Kestrel 5000"],
      ["R2", "Solar bias", "≤ 0.5 °C mean bias in daytime GH1 (proposed)", "Unshielded bias was +4.3 °C, as large as the spread", "Shielded node vs reference in sun"],
      ["R3", "Durability in humidity", "≥ 14 days in GH1 with misting; ≥ 95% valid readings after cleaning", "High night-time humidity and daily misting", "Field deployment log"],
      ["R4", "Simultaneous sampling", "All nodes sampled within the same 60 s window; ≥ 99% of packets delivered over 30 days", "Temperature changes within minutes, so readings taken at different times cannot be compared", "Timestamp and sequence-number checks"],
      ["R5", "Hotspot detection", "Permanent nodes find the hottest crop zone identified by the full temporary grid in ≥ 80% of test periods (proposed)", "Sets the number of permanent nodes without over-instrumenting", "Held-out comparison with the temporary grid"],
      ["R6", "Soft-sensor accuracy", "Estimates at removed temporary-node locations within 1.0 °C and 5 %RH RMSE (proposed)", "Lets temporary nodes be removed after training, cutting sensor cost", "Train on one period, test on another"],
      { group: "O2 Cooling layout evaluation" },
      ["R7", "Layout validation", "Layouts suggested by simulation reduce measured crop-zone exceedance against the baseline, in the order predicted", "Confirms the simulation's advice on crop temperature, where it matters", "Suggested layouts built with the floor fans; temperature measured under comparable weather"],
      ["R8", "Configuration study", "≥ 10 fan configurations compared with baseline in simulation; top ≥ 3 suggestions tested with 4 floor fans (proposed)", "Enough to show trends and a best option", "Simulation runs and test-section trials"],
      { group: "O3 Targeted cooling" },
      ["R9", "Hotspot prediction", "Forecasts crop-zone exceedance for the next 30 min, updated every 30 min; flags ≥ 80% of measured exceedance periods (proposed)", "Cooling can start before hotspots form rather than after", "Predicted vs measured exceedance over test days"],
      ["R10", "Hotspot reduction", "Crop-zone exceedance (°C·min above 29 °C) ≥ 20% lower than baseline (proposed)", "Primary measure of thermal benefit", "Alternating-day trials under comparable weather"],
      ["R11", "Energy use", "Fan energy ≤ baseline for equal or better exceedance", "Cooling must not cost more to run than today", "Fan energy metering"],
      ["R12", "Correct and fail-safe actuation", "Fans that most affect a predicted hotspot switch on in ≥ 90% of events (proposed); fans revert to baseline on any fault; minimum on/off time ≥ 10 min", "Shows the twin drives the right fans; protects crops and equipment", "Logged predictions vs fan commands; fault-injection test"],
      ["R13", "Dashboard update", "Map, hotspots and fan states refreshed ≤ 1 min after each 30-min sample", "Operators need current information", "Timed test on site"],
      ["R14", "Offline operation", "Runs without internet, using sensor data alone; restarts ≤ 5 min after power loss", "Rural farms may have limited connectivity", "Network-unplug and power-cycle tests"],
    ],
  },

  // Table 8: Subsystem goals (Section 6.2)
  "table-subsystems": {
    columns: ["Subsystem", "Goal", "Deliverables", "Verified by"],
    data: [
      ["S1 Sense and Map", "Synchronised, location-tagged crop-zone T/RH and canopy temperature, mapped between nodes with fewer sensors", "Type A/B nodes, shielded enclosure, RS-485 network, permanent and temporary nodes, gateway logging; 30-min sampling with median-centred averaging; data cleaning, soft-sensor models, Gaussian process regression map", "R1–R6"],
      ["S2 Cooling Layout Evaluation (Application 1)", "Suggest fan layouts that lower crop-zone exceedance, confirmed by measured temperature", "CFD model with measured inputs; ranked layout suggestions; test-section trials with four floor fans", "R7, R8"],
      ["S3 Live Cooling Control (Application 2)", "Predict hotspots 30 min ahead and run the fans that most affect them, safely and without extra energy", "Prediction and fan-effect models; prediction-triggered rules with fail-safe; four floor fans with speed/relay interface and energy metering; dashboard", "R9–R14"],
    ],
  },

  // Table 6: Concept selection (Section 4.2)
  "table-concepts": {
    columns: ["Function", "Decision", "Options considered", "Selected", "Reason"],
    data: [
      { group: "O1 Thermal characterisation" },
      ["Capture readings at the same time", "Sensor-to-gateway link", "RS-485, Wi-Fi, BLE, Zigbee, LoRa", "RS-485, wireless option benchmarked", "Robust over ~57 m and already verified end-to-end; wireless avoids cabling but needs reliability and power testing"],
      ["Clean the data", "Edge computer", "Raspberry Pi 5, laptop, cloud", "Raspberry Pi 5", "Low cost and power: runs Docker, MQTT and Node-RED locally"],
      ["Map the distribution", "Thermal map method", "Permanent grid inverse-distance weighting. Gaussian process regression: soft sensors trained on temporary nodes", "Soft sensors, with Gaussian process regression between nodes", "Fewer permanent nodes after training. Gaussian process regression shows where uncertainty remains"],
      { group: "O2 Cooling layout evaluation" },
      ["Estimate airflow", "Airflow method", "CFD; dense airspeed survey, empirical fan-jet estimates", "Offline CFD with measured inputs (roof temperature, fan flow, geometry)", "Airflow cannot be measured densely; CFD can evaluate layouts before they are installed"],
      ["Estimate heat distribution", "Heat-distribution method", "CFD only, measured data only; both", "CFD for candidate layouts; suggested layouts confirmed by measured temperature in real-life tests", "Layouts can be compared before installation; real tests confirm the improvement where it matters"],
      ["Estimate airflow", "CFD tool", "SOLIDWORKS Flow Simulation; ANSYS Fluent; OpenFOAM", "SOLIDWORKS Flow Simulation", "Integrated with the CAD model and available; adequate for comparative studies"],
      { group: "O3 Targeted cooling" },
      ["Forecast hotspots", "Prediction inputs", "On-site sensors only, weather readings, forecast service", "On-site sensors, supported by NEA live readings and 2-hour nowcast", "Crop-zone sensors show actual conditions, weather data gives early warning of sun or rain. Prediction still runs on sensors alone when offline"],
      ["Decide the cooling action", "Controller", "PID; reactive rules; rules triggered by 30-min predictions; model predictive control", "Rules triggered by 30-min predictions (MPC as stretch)", "Starts the fans the twin has learned affect each zone, before hotspots form; transparent and testable"],
      ["Operate the fans", "Actuation", "Modify ventilation or misting, control existing fans; procure own floor fans", "Procure floor circulation fans", "Existing systems cannot be modified, own fans are safe, movable and allow speed tests"],
    ],
  },

  // Table 9: S1 detailed design (Section 6.3.1)
  "table-s1-design": {
    columns: ["Objective", "Detailed design", "Deliverable"],
    data: [
      ["Measure air temperature and humidity", "Type A node: ESP32-C6 with an SHT45 in a ventilated, louvred shield, separated from the electronics. Every 30 min, 60 readings over 1 min; the mean of the 20 closest to the median is reported", "Type A nodes for the main grid (R1, R2)"],
      ["Measure canopy leaf temperature", "Type B node: adds an MLX90640 thermal camera (32 × 24 pixels) aimed at the leaves: 10 frames averaged, emissivity 0.95", "Type B nodes at fewer locations"],
      ["Survive greenhouse conditions", "Enclosure with a separate electronics and battery compartment; power supply (wired DC or battery) chosen in Semester 2", "Durable enclosure (R3)"],
      ["Sample all nodes together", "RS-485 (9600 baud, 8N1); JSON packets with node ID, sequence number and readings, to a USB–RS-485 adapter on the Raspberry Pi 5", "RS-485 network (R4)"],
      ["Store and clean the data", "Docker on the Pi runs a Mosquitto MQTT broker and Node-RED to time-stamp the data and remove spikes and misting artefacts; InfluxDB planned for storage", "Edge gateway and data pipeline (Figure 14)"],
      ["Map conditions with fewer sensors", "Temporary nodes during training; soft sensors estimate their readings from permanent nodes, fan states and outdoor conditions; Gaussian process regression fills the gaps between nodes with uncertainty", "Soft-sensor models and thermal map (R5, R6)"],
    ],
  },

  // Table 12: S2 detailed design (Section 6.4.1)
  "table-s2-design": {
    columns: ["Objective", "Detailed design", "Deliverable"],
    data: [
      ["Model GH1", "SOLIDWORKS Flow Simulation; geometry, roof, walls and netting as built (Appendix D); existing ventilation and ceiling fans at rated airflow as the baseline (Appendix E); measured roof surface temperature replaces a full solar-radiation model; crops modelled as a porous zone", "Full-GH1 CAD geometry built (Figure 20); test-section (germination section) and full-GH1 flow models"],
      ["Compare fan layouts", "1–4 floor fans in the test section, more in full-GH1 runs; positions, direction and speed varied; representative midday, morning and overcast cases. Outputs: airflow, crop-zone temperature, exceedance H, fan power", "≥ 10 configurations ranked against the baseline (R8)"],
      ["Confirm the suggestions", "Top suggested layouts built with the four floor fans in the germination section; measured crop-zone temperature compared with the baseline under comparable weather; judged on trends and rankings, not absolute temperatures", "Validated layout ranking (R7)"],
    ],
  },

  // Table 13: S3 detailed design (Section 6.5.1)
  "table-s3-design": {
    columns: ["Objective", "Detailed design", "Deliverable"],
    data: [
      ["Learn fan effects", "From logged S1 data, a model learns how each fan setting changes temperature and humidity in each zone", "Fan-effect model"],
      ["Predict hotspots", "Every 30 min, a prediction model uses the thermal map, supported by NEA live readings and the 2-hour nowcast, to forecast crop-zone exceedance H for the next 30 min; runs on sensor data alone without internet", "Prediction model (R9, R14)"],
      ["Decide fan actions", "When a zone's predicted H rises above a threshold, the fans that most affect it switch on or speed up; they return to low speed or off when H is predicted to fall; minimum on/off time ≥ 10 min", "Rule-based controller (R10, R12)"],
      ["Fail safely", "If sensors or the controller fail, the fans revert to baseline operation (on)", "Fail-safe logic (R12)"],
      ["Run and meter the fans", "Four floor circulation fans, ideally low-voltage DC with PWM speed control so the farm's mains wiring is unchanged; fan energy metered", "Fan interface and energy log (R11)"],
      ["Show status", "Grafana dashboard on the Pi showing the map, predictions and fan status", "Dashboard (R13)"],
    ],
  },

  // Table 10: SHT45 vs Kestrel 5000 (Section 6.3.3)
  "table-sht45": {
    columns: ["Test", "Quantity", "Mean error", "MAE", "RMSE"],
    data: [
      ["Bench (~10 min)", "Temperature", "+0.10 °C", "0.22 °C", "0.33 °C"],
      ["Bench (~10 min)", "Relative humidity", "+0.69 %RH", "1.62 %RH", "2.35 %RH"],
      ["GH1 (~30 min)", "Temperature", "+4.28 °C", "4.28 °C", "4.77 °C"],
      ["GH1 (~30 min)", "Relative humidity", "−10.02 %RH", "10.02 %RH", "10.53 %RH"],
    ],
  },

  // Table 11: MLX90640 vs handheld thermal camera (Section 6.3.3)
  "table-mlx": {
    columns: ["Distance", "MLX90640 centre", "Reference centre", "Difference", "MLX90640 max", "Reference max"],
    data: [
      ["50 mm", "33.5 °C", "33.8 °C", "−0.3 °C", "35.6 °C", "38.3 °C"],
      ["100 mm", "34.0 °C", "35.3 °C", "−1.3 °C", "38.1 °C", "41.9 °C"],
      ["400 mm", "33.3 °C", "33.3 °C", "0.0 °C", "38.7 °C", "40.5 °C"],
      ["500 mm", "33.3 °C", "32.9 °C", "+0.4 °C", "38.6 °C", "40.8 °C"],
    ],
  },

  // Table 15: Milestones (Section 7.4)
  "table-milestones": {
    columns: ["Milestone", "Date", "Deliverable", "Acceptance criterion"],
    data: [
      ["M1", "31 Dec 2026", "Sensor nodes fabricated with shielded enclosures", "R1 and R2 met on the fabricated nodes"],
      ["M2", "31 Jan 2027", "Permanent and temporary nodes deployed in the test section; test-section CFD model built", "R4 met over the first 7 days; CFD ready for the floor-fan tests"],
      ["M3", "21 Feb 2027", "Floor-fan tests in the test section; soft sensors trained", "Suggested layouts tested and improvement confirmed (R7); soft sensors meet R6"],
      ["M4", "14 Mar 2027", "Full-GH1 configuration study; prediction, control loop and dashboard working", "≥ 10 configurations ranked (R8); predictions meet R9; correct, fail-safe actuation and dashboard live (R12, R13)"],
      ["M5", "11 Apr 2027", "Validation complete", "Baseline vs proposed trials report exceedance and fan energy (R10, R11); hotspot detection (R5); durability ≥ 14 days (R3)"],
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

  // Table 3: 57-point survey (Section 2.3)
  "table-survey": {
    columns: ["s (m)", "Row 1", "Row 2", "Row 3"],
    data: [
      ["1.5", "T1 36.1", "T2 36.4", "T3 37.0"],
      ["4.6", "T4 37.0", "T5 36.8", "T6 37.0"],
      ["7.7", "T7 38.0", "T8 35.6", "T9 37.6"],
      ["10.8", "T10 38.2", "T11 35.7", "T12 38.1"],
      ["13.9", "T13 38.2", "T14 35.5", "T15 37.9"],
      ["17.0", "T16 37.7", "T17 35.7", "T18 39.2"],
      ["20.1", "T19 37.7", "T20 36.0", "T21 39.2"],
      ["23.2", "T22 36.9", "T23 37.0", "T24 39.1"],
      ["26.3", "T25 37.0", "T26 37.1", "T27 39.1"],
      ["29.4", "T28 37.2", "T29 37.5", "T30 38.8"],
      ["32.5", "T31 37.5", "T32 37.7", "T33 38.9"],
      ["35.6", "T34 37.8", "T35 38.0", "T36 38.0"],
      ["38.7", "T37 38.8", "T38 38.9", "T39 39.0"],
      ["41.8", "T40 38.8", "T41 39.4", "T42 39.0"],
      ["44.9", "T43 38.5", "T44 39.0", "T45 39.1"],
      ["48.0", "T46 38.8", "T47 39.0", "T48 39.1"],
      ["51.1", "T49 39.1", "T50 39.2", "T51 39.0"],
      ["54.2", "T52 39.4", "T53 39.5", "T54 38.5"],
      ["57.3", "T55 39.4", "T56 39.3", "T57 38.5"],
    ],
  },

  // Table A4: GH1 geometry (Appendix D)
  "table-geometry": {
    columns: ["Item", "Value", "Source"],
    data: [
      ["Width", "12.5 m", "Layout"],
      ["Main section", "36 m straight", "Layout"],
      ["Transition walls", "3.67 m (top), 2.48 m (bottom)", "Layout"],
      ["Wing walls", "19.53 m (top), 20.5 m (bottom)", "Layout"],
      ["Bend angle", "5.46°, toward the bottom of the layout", "Derived from the transition wall lengths"],
      ["Centreline length", "59.1 m", "Derived from the wall labels"],
      ["Wall height", "3.00 m", "Table, front sketch"],
      ["Main ridge height", "3.35 m", "Front sketch"],
      ["Raised ridge section", "about 3 m wide, full length, top at 4.35 m (confirmed); shoulder at 3.95 m (assumed)", "Sketch and table"],
      ["Base kerb", "0.29 m", "Front sketch"],
      ["Walls, lower half", "Insect netting, 0.3 mm, from the kerb to 1.5 m", "Confirmed"],
      ["Walls, upper half", "Clear plastic, 0.3 mm, with 0.5 mm shading over it, 1.5 to 3.0 m", "Confirmed"],
      ["Roof", "Same clear plastic and shading as the upper walls", "Confirmed"],
      ["Front airlock", "2.4 m wide, 2.3 m high, 1.5 m deep, t = 3.7 to 6.1 m", "Sketch, depth assumed"],
      ["Floor hump", "Old road hump, 2.1 m wide, arc profile, 150 mm at the peak, at s = 20 m", "Confirmed; position from the layout"],
      ["Plant height", "1.0 m", "Sketch note"],
    ],
  },
  // Table A5
  "table-fans": {
    columns: ["Fan", "Type", "s (m)", "t (m)", "Direction"],
    data: [
      ["1", "Wall exhaust, front", "0", "5.8", "Out"],
      ["2", "Wall exhaust, front", "0", "3.07", "Out"],
      ["3", "Ceiling circulating", "5.6", "8.1", "Toward rear"],
      ["4", "Ceiling circulating", "16.0", "4.1", "Toward front"],
      ["5", "Ceiling circulating", "28.8", "8.1", "Toward rear"],
      ["6", "Ceiling circulating", "43.3", "4.1", "Toward front"],
      ["7", "Ceiling circulating", "45.7", "8.1", "Toward rear"],
      ["8", "Ceiling circulating", "54.8", "4.1", "Toward front"],
      ["9", "Wall exhaust, rear", "End", "6.2", "Out"],
      ["10", "Wall exhaust, rear", "End", "3.9", "Out"],
    ],
  },
};

// Called by report-loader.js once the sections are on the page.
// A cell can be plain text, or { img: "assets/..." } to show a photo in the cell.
// A table can also have a "note": HTML shown as a full-width box under the table.
// Group rows: write { group: "Label" } in a table's data to start a labelled band of rows.
function groupRow(label, ncols) {
  return [gridjs.html(`<span class="table-group">${label}</span>`), ...Array(ncols - 1).fill("")];
}

function renderCell(cell, row) {
  if (cell && typeof cell === "object" && cell.img) {
    const alt = String(row[0]).replace(/"/g, "&quot;");
    return gridjs.html(`<img class="cell-img" src="${cell.img}" alt="${alt}">`);
  }
  return cell;
}

function renderReportTables() {
  for (const [id, config] of Object.entries(tables)) {
    const el = document.getElementById(id);
    if (el && !el.hasChildNodes()) {
      const { note, ...gridConfig } = config;
      const data = config.data.map((row) =>
        Array.isArray(row) ? row.map((cell) => renderCell(cell, row)) : groupRow(row.group, config.columns.length)
      );
      const gridTarget = document.createElement("div");
      el.appendChild(gridTarget);
      new gridjs.Grid({ ...gridConfig, data, sort: false }).render(gridTarget);
      // Optional full-width note under the table (HTML), e.g. Table 2's "Current Use".
      if (note) {
        const noteEl = document.createElement("div");
        noteEl.className = "table-note";
        noteEl.innerHTML = note;
        el.appendChild(noteEl);
      }
    }
  }
}
