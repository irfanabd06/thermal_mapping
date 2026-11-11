// Data for the report's Grid.js tables.
// Edit the arrays here; each table renders into the <div> with the matching id in index.html.

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
      ["Ventilation fans", "4 (running 24/7)"],
      ["Ceiling circulation fans", "6 (running 24/7)"],
      ["Floor circulation fans", "Installed, not in use"],
      ["Misting", "Operates throughout the day"],
      ["Crops", "Lettuce, kai lan, bak choi, basil and others"],
    ],
  },

  // Table 2: Problem → solution map (Section 3.2)
  "table-problem-solution": {
    columns: ["Target problem (evidence)", "Solution", "Objective", "Requirements"],
    data: [
      [
        "P1. Single-point monitoring misses spatial variation (4.0 °C spread across 57 points; one monitoring point in GH1)",
        "Distributed sensor network + Gaussian-process thermal map with uncertainty",
        "O1 Spatial monitoring",
        "R1–R7",
      ],
      [
        "P2. No way to predict conditions or test changes before installing them",
        "Two-model digital twin: CFD for spatial patterns, zone model for dynamics, calibrated to sensors",
        "O2 Validated model",
        "R8–R10",
      ],
      [
        "P3. Fans and vents placed without analysis",
        "CFD placement study + surrogate model and Bayesian optimisation",
        "O3 Placement (where)",
        "R11",
      ],
      [
        "P4. Fans run continuously without spatial or timing logic (4 ventilation + 6 ceiling fans always on; high operating cost)",
        "Spatially informed fan scheduling on the Raspberry Pi 5, validated with procured floor fans",
        "O4 Timing (when)",
        "R12–R16",
      ],
    ],
  },

  // Table 3: Technical requirements and targets (Section 4)
  // DRAFT targets: confirm with supervisor and adjust from bench data.
  "table-requirements": {
    columns: ["ID", "Requirement", "Target", "Rationale", "Verification", "Status"],
    data: [
      ["R1", "Air temperature accuracy", "≤ ±0.3 °C after calibration", "SHT45 ~±0.1 °C typical; margin for shield and self-heating; far below the 4 °C spread", "24 h side-by-side with reference", "Not tested"],
      ["R2", "RH accuracy", "≤ ±3 %RH", "SHT45 ~±1 %RH typical; margin for condensation and misting", "As R1", "Not tested"],
      ["R3", "Radiation-shield bias", "≤ 0.5 °C in direct sun", "Unshielded sensors can read several °C high", "Shielded vs reference, sun and shade", "Not tested"],
      ["R4", "Sampling interval", "T/RH ≤ 60 s; thermal frame ≤ 5 min", "Fan responses over minutes; 768-pixel frames costly to store", "Gateway logs", "60 s on bench"],
      ["R5", "Data delivery", "≥ 99% wired, ≥ 95% wireless over 7 days; latency ≤ 5 s", "Gaps break the map and the controller", "Sequence-number counts", "Short test passed"],
      ["R6", "Map accuracy", "≤ 0.5 °C MAE at held-out nodes", "Must resolve differences within the 4 °C spread; sets node spacing", "Leave-one-out cross-validation", "Not tested"],
      ["R7", "Environmental robustness", "20–50 °C, ≤ 100 %RH; enclosure ≥ IP54; 7 days unattended", "45 °C reported peak; 87.5 % night RH; daily misting", "Field deployment log", "Not tested"],
      ["R8", "CFD temperature accuracy", "≤ 1.5 °C MAE on a day not used for calibration; hottest zone identified", "Published greenhouse models report 1.74–2.04 °C RMSE", "Predicted vs measured", "Not started"],
      ["R9", "Fan-influence ranking", "Matches step tests in ≥ 80% of zones", "Placement advice depends on ranking", "Fan step tests", "Not started"],
      ["R10", "Zone-model forecast", "≤ 0.5 °C error at 30 min ahead", "Needed to time fan activation", "Hold-out days", "Not started"],
      ["R11", "Placement study", "≥ 10 configurations ranked by σT, max zone temperature, fan power", "Enough to show a trend and a best option", "CFD runs + sensitivity check", "Not started"],
      ["R12", "Control performance", "vs continuous: exceedance time or σT −20%, or equal with −30% fan-hours", "Fans redistribute heat; realistic gains are uniformity and energy", "Alternating-day trials, weather-normalised", "Not started"],
      ["R13", "Anti-cycling", "Minimum on/off time ≥ 10 min", "Limits wear and oscillation", "Controller logs", "Not started"],
      ["R14", "Fail-safe", "Fans default ON on fault; manual override", "Crop safety first", "Fault-injection test", "Not started"],
      ["R15", "Electrical safety", "Fans ≤ 24 V DC or certified plug-in switching; no changes to farm mains", "Safe, reversible installation", "Design review", "Not started"],
      ["R16", "Local-first operation", "Runs without internet; auto-restart ≤ 5 min after power loss", "Limited connectivity on site", "Network-unplug and power-cycle tests", "Not tested"],
    ],
  },
};

for (const [id, config] of Object.entries(tables)) {
  const el = document.getElementById(id);
  if (el) {
    new gridjs.Grid({ ...config, sort: false }).render(el);
  }
}
