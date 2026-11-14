# Greenhouse 1 thermal map dashboard

Source for the 3D thermal map dashboard and the greenhouse CAD model.

- Published page: `docs/dashboard/index.html`, served by GitHub Pages at <https://irfanabd06.github.io/thermal_mapping/dashboard/>
- CAD model: `cad/Greenhouse1.step` (millimetres, Z up, 79 named bodies)

Both are generated from the files in this folder. Edit the sources here, then rebuild.

## Files

| File | What it is |
|---|---|
| `template.html` | The dashboard source: layout (HTML), styling (CSS) and behaviour (JavaScript). |
| `build_model.py` | The greenhouse geometry. Writes the STEP file and the model the page reads. |
| `survey.txt` | The 57 temperature readings from the preliminary survey, one per line. |
| `build_page.py` | Puts the model and the readings into `template.html`. |
| `verify_step.py` | Reads the STEP file back and checks every body is closed and planar. |
| `build.py` | Runs all of the above and copies the results into `docs/dashboard/` and `cad/`. |

## Rebuilding after an edit

Python 3 only, no extra packages:

```bash
python dashboard/build.py
```

Then open `docs/dashboard/index.html` in a browser, and commit the changed files.

## Where to change common things

| To change | Edit |
|---|---|
| Readings | `survey.txt` |
| Target temperature (default 29) | `target: 29.0` in the `state` line of `template.html` |
| Default hotspot limit (39.0) | `thr: 39.0` in the same line |
| Wall lengths, heights, hump, beds, fans | The constants and lists at the top of `build_model.py` |
| Measurement grid spacing | `S0`, `DS`, `DT` in `build_model.py` |
| Site coordinates for weather and sun | `SITE` in `template.html` |
| Colours and fonts | The `:root` block at the top of `template.html` |

## How the page is organised (`template.html`)

The script is in sections, each under a comment heading:

1. **state**: the readings, target, hotspot limit and view mode.
2. **geometry mapping**: turns "distance along the house, distance across" into plan coordinates, including the bend.
3. **colour ramps**: temperature to colour.
4. **statistics, interpolation**: mean, max, min, and the smooth surface between the 57 points.
5. **hot zones**: groups neighbouring points above the hotspot limit.
6. **WebGL**: draws the 3D model in plain WebGL, with no library.
7. **overlay**: the measurement dots and labels placed over the 3D view.
8. **panels, profile chart**: tiles, tables and the chart, built as HTML and SVG.
9. **site, sun and weather**: sun position by formula, weather from Open-Meteo.
10. **refresh, data API**: the functions other programs call.
11. **tabs**: switches between the Monitoring and 3D map tabs (`#monitoring`, `#map-3d`).

## Feeding it live data

The page exposes one object, `Greenhouse`:

```js
Greenhouse.update({ T1: 36.4, T2: 36.2 }, { source: "Live sensors", meta: "updated 10:42", live: true });
Greenhouse.setTarget(29);
Greenhouse.setWeather({ temp: 31.2, rh: 68, wind: 1.4, dir: 40, solar: 610, rain: 0, source: "Rooftop weather station" });
Greenhouse.sensors   // ids and positions of the 57 points
```

## Limits to know about

- The readings are one walk-through survey with no time stamps. The map is interpolated between 57 points at 1 m height.
- The weather is a forecast model value for the location (Open-Meteo), not a measurement on the roof. It needs internet access.
- The STEP file is checked by `verify_step.py` only. Confirm it opens correctly in SOLIDWORKS.
- Wall and roof panels are a nominal 20 mm thick in the CAD model. The real film thicknesses (0.3 mm netting and plastic, 0.5 mm shading) are in the body names.
- Bed widths, tank and station sizes, and fan heights are scaled from the layout drawing and photos.
