
import csv
import json
import re
from pathlib import Path
from datetime import datetime, timezone

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import RectangleSelector
import serial

# ==========================================
# CONFIGURATION
# ==========================================

PORT = "COM7"
BAUD = 115200

WIDTH = 32
HEIGHT = 24

ROTATION = 1
FLIP_HORIZONTAL = FALSE

BASE_DIR = Path(__file__).resolve().parent
RESULTS_DIR = BASE_DIR / "results"

# ==========================================
# IMAGE ORIENTATION
# ==========================================

def orient(frame):
    result = np.rot90(frame, k=ROTATION)

    if FLIP_HORIZONTAL:
        result = np.fliplr(result)

    return result


# ==========================================
# CREATE NEXT POINT FOLDER
# ==========================================

def next_point_folder():
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    numbers = []

    for folder in RESULTS_DIR.iterdir():
        match = re.fullmatch(
            r"point_(\d+)",
            folder.name
        )

        if folder.is_dir() and match:
            numbers.append(int(match.group(1)))

    number = max(numbers, default=0) + 1
    folder = RESULTS_DIR / f"point_{number:03d}"
    folder.mkdir(exist_ok=False)

    return folder


# ==========================================
# LIVE DATA
# ==========================================

air_temperature = None
relative_humidity = None

latest_raw_frame = None
latest_display_frame = None

roi = None
roi_stats = None

# ==========================================
# SETUP MATPLOTLIB
# ==========================================

plt.ion()

fig, ax = plt.subplots(figsize=(10, 7))
fig.subplots_adjust(bottom=0.20, top=0.87)

initial = np.zeros((WIDTH, HEIGHT))

image = ax.imshow(
    initial,
    cmap="inferno",
    interpolation="nearest",
    origin="upper",
    vmin=25,
    vmax=40
)

fig.colorbar(
    image,
    ax=ax,
    label="Surface temperature (°C)"
)

ax.set_title("MLX90640 Live Thermal Camera")
ax.set_xlabel("Pixel column")
ax.set_ylabel("Pixel row")

sht_text = fig.text(
    0.5,
    0.10,
    "SHT45 | Waiting for measurements...",
    ha="center",
    fontsize=12
)

status_text = fig.text(
    0.5,
    0.04,
    "Drag to select ROI | Press S to save point",
    ha="center",
    fontsize=10
)


# ==========================================
# ROI SELECTION
# ==========================================

def calculate_roi_stats(frame):
    global roi_stats

    if roi is None:
        roi_stats = None
        return

    x1, x2, y1, y2 = roi

    height, width = frame.shape

    x1 = max(0, min(x1, width - 1))
    x2 = max(0, min(x2, width - 1))
    y1 = max(0, min(y1, height - 1))
    y2 = max(0, min(y2, height - 1))

    selected = frame[
        y1:y2 + 1,
        x1:x2 + 1
    ]

    valid = selected[np.isfinite(selected)]

    if valid.size == 0:
        roi_stats = None
        return

    roi_stats = {
        "mean_c": float(np.mean(valid)),
        "median_c": float(np.median(valid)),
        "min_c": float(np.min(valid)),
        "max_c": float(np.max(valid)),
        "pixel_count": int(valid.size)
    }


def on_select(eclick, erelease):
    global roi

    if (
        eclick.xdata is None or
        eclick.ydata is None or
        erelease.xdata is None or
        erelease.ydata is None
    ):
        return

    x1, x2 = sorted([
        int(round(eclick.xdata)),
        int(round(erelease.xdata))
    ])

    y1, y2 = sorted([
        int(round(eclick.ydata)),
        int(round(erelease.ydata))
    ])

    roi = (x1, x2, y1, y2)

    if latest_display_frame is not None:
        calculate_roi_stats(latest_display_frame)


selector = RectangleSelector(
    ax,
    on_select,
    useblit=True,
    button=[1],
    interactive=True
)


# ==========================================
# SAVE CURRENT CALIBRATION POINT
# ==========================================

def save_point():
    if latest_raw_frame is None:
        print("No thermal frame available yet.")
        return

    folder = next_point_folder()

    timestamp = datetime.now(
        timezone.utc
    ).isoformat()

    # Preserve unrotated original thermal data.
    np.save(
        folder / "mlx90640_frame.npy",
        latest_raw_frame
    )

    np.savetxt(
        folder / "mlx90640_frame.csv",
        latest_raw_frame,
        delimiter=",",
        fmt="%.4f"
    )

    # Save current SHT45 reading.
    with open(
        folder / "sht45_reading.csv",
        "w",
        newline="",
        encoding="utf-8"
    ) as f:
        writer = csv.writer(f)

        writer.writerow([
            "timestamp_utc",
            "temperature_c",
            "humidity_rh"
        ])

        writer.writerow([
            timestamp,
            air_temperature,
            relative_humidity
        ])

    metadata = {
        "timestamp_utc": timestamp,
        "port": PORT,
        "baud_rate": BAUD,
        "mlx_mode": "interleaved",
        "emissivity": 0.95,
        "reflected_temperature_assumption": "Ta - 8 C",
        "resolution": [HEIGHT, WIDTH],
        "rotation_k": ROTATION,
        "flip_horizontal": FLIP_HORIZONTAL,
        "sht45_temperature_c": air_temperature,
        "sht45_humidity_rh": relative_humidity,
        "roi_display_coordinates": roi,
        "roi_statistics": roi_stats
    }

    (folder / "metadata.json").write_text(
        json.dumps(metadata, indent=2),
        encoding="utf-8"
    )

    # Save the current thermal image.
    fig.savefig(
        folder / "thermal_interleaved.png",
        dpi=200
    )

    print(f"\nSaved calibration point: {folder}")

    status_text.set_text(
        f"Saved: {folder.name} | Press S for next point"
    )

    fig.canvas.draw_idle()


# ==========================================
# KEYBOARD SHORTCUTS
# ==========================================

def on_key(event):
    if event.key is None:
        return

    if event.key.lower() == "s":
        save_point()


fig.canvas.mpl_connect(
    "key_press_event",
    on_key
)


# ==========================================
# UPDATE THERMAL DISPLAY
# ==========================================

def update_thermal_display(raw_frame):
    global latest_raw_frame
    global latest_display_frame

    latest_raw_frame = raw_frame.copy()
    latest_display_frame = orient(raw_frame)

    image.set_data(latest_display_frame)

    valid = latest_display_frame[
        np.isfinite(latest_display_frame)
    ]

    if roi is not None:
        calculate_roi_stats(latest_display_frame)

    if roi_stats is not None:
        ax.set_title(
            "MLX90640 Live | "
            f"ROI Mean: {roi_stats['mean_c']:.2f} °C | "
            f"Median: {roi_stats['median_c']:.2f} °C | "
            f"Min: {roi_stats['min_c']:.2f} °C | "
            f"Max: {roi_stats['max_c']:.2f} °C"
        )
    elif valid.size:
        ax.set_title(
            "MLX90640 Live | "
            f"Min: {np.min(valid):.2f} °C | "
            f"Max: {np.max(valid):.2f} °C"
        )

    fig.canvas.draw_idle()


# ==========================================
# SERIAL RECEIVER
# ==========================================

def main():
    global air_temperature
    global relative_humidity

    print(f"Connecting to ESP32-C6 on {PORT}...")

    with serial.Serial(
        PORT,
        BAUD,
        timeout=0.2
    ) as ser:

        print("Waiting for live sensor data...")

        while plt.fignum_exists(fig.number):
            raw = ser.readline()

            if not raw:
                plt.pause(0.001)
                continue

            line = raw.decode(
                "utf-8",
                errors="replace"
            ).strip()

            # ------------------------------
            # SHT45
            # ------------------------------

            if line.startswith("SHT45,"):
                parts = line.split(",")

                if len(parts) == 3:
                    try:
                        air_temperature = float(parts[1])
                        relative_humidity = float(parts[2])

                        sht_text.set_text(
                            f"SHT45 Air: {air_temperature:.2f} °C"
                            f"   |   "
                            f"RH: {relative_humidity:.2f} %"
                        )

                        fig.canvas.draw_idle()

                    except ValueError:
                        pass

                plt.pause(0.001)
                continue

            if line == "SHT45_INVALID":
                sht_text.set_text(
                    "SHT45 | Invalid reading"
                )
                plt.pause(0.001)
                continue

            # ------------------------------
            # MLX90640
            # ------------------------------

            if line != "FRAME_START":
                plt.pause(0.001)
                continue

            rows = []
            valid_frame = True

            for _ in range(HEIGHT):
                raw_row = ser.readline()

                if not raw_row:
                    valid_frame = False
                    break

                row_text = raw_row.decode(
                    "utf-8",
                    errors="replace"
                ).strip()

                try:
                    values = np.array(
                        [
                            float(value)
                            for value in row_text.split(",")
                        ],
                        dtype=np.float32
                    )
                except ValueError:
                    valid_frame = False
                    break

                if len(values) != WIDTH:
                    valid_frame = False
                    break

                rows.append(values)

            if not valid_frame:
                continue

            ending = ser.readline().decode(
                "utf-8",
                errors="replace"
            ).strip()

            if ending != "FRAME_END":
                continue

            frame = np.array(
                rows,
                dtype=np.float32
            )

            if frame.shape != (HEIGHT, WIDTH):
                continue

            update_thermal_display(frame)
            plt.pause(0.001)


if __name__ == "__main__":
    try:
        main()

    except KeyboardInterrupt:
        print("\nLive viewer stopped.")

    except serial.SerialException as error:
        print("Serial error:", error)

    finally:
        plt.close("all")
