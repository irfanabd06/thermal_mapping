
import csv
import json
import re
import time
from pathlib import Path
from datetime import datetime, timezone

import numpy as np
import matplotlib.pyplot as plt
import serial

# ==========================================
# CONFIGURATION
# ==========================================

PORT = "COM7"
BAUD_RATE = 115200

SHT_COUNT = 10
FRAME_COUNT = 10
WIDTH = 32
HEIGHT = 24

TIMEOUT_SECONDS = 90

BASE_DIR = Path(__file__).resolve().parent
RESULTS_DIR = BASE_DIR / "results"

# Display orientation from previous tests
ROTATION = 1
FLIP_HORIZONTAL = True


# ==========================================
# CREATE NEXT CALIBRATION FOLDER
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
# RECEIVE CALIBRATION DATA
# ==========================================

def capture_from_esp32():
    sht_samples = []
    frames = {}
    frame_timestamps = {}

    metadata = {
        "capture_started_at": datetime.now(
            timezone.utc
        ).isoformat(),
        "port": PORT,
        "baud_rate": BAUD_RATE
    }

    print(f"Connecting to ESP32 on {PORT}...")

    with serial.Serial(
        PORT,
        BAUD_RATE,
        timeout=1,
        write_timeout=5
    ) as ser:

        # CP210x opening may reset the ESP32.
        time.sleep(3)

        ser.reset_input_buffer()

        print("Sending CAPTURE command...")
        ser.write(b"CAPTURE\n")
        ser.flush()

        deadline = time.monotonic() + TIMEOUT_SECONDS

        started = False
        completed = False

        while time.monotonic() < deadline:
            raw = ser.readline()

            if not raw:
                continue

            line = raw.decode(
                "utf-8",
                errors="replace"
            ).strip()

            if not started:
                if line == "CAL_START":
                    started = True
                    print("Calibration started.")
                continue

            if line == "CAL_END":
                completed = True
                break

            if line.startswith("CAL_MODE,"):
                metadata["mlx_mode"] = line.split(
                    ",", 1
                )[1]

            elif line.startswith("CAL_EMISSIVITY,"):
                metadata["emissivity"] = float(
                    line.split(",")[1]
                )

            elif line.startswith("CAL_REFLECTED_TEMP,"):
                metadata["reflected_temperature"] = (
                    line.split(",", 1)[1]
                )

            elif line.startswith("SHT,"):
                parts = line.split(",")

                if len(parts) != 5:
                    raise ValueError(
                        f"Invalid SHT record: {line}"
                    )

                sht_samples.append({
                    "sample": int(parts[1]),
                    "uptime_ms": int(parts[2]),
                    "temperature_c": float(parts[3]),
                    "humidity_rh": float(parts[4])
                })

                print(
                    f"SHT45: {len(sht_samples)}/{SHT_COUNT}"
                )

            elif line.startswith("SHT_INVALID,"):
                raise RuntimeError(
                    f"SHT45 measurement failed: {line}"
                )

            elif line.startswith("FRAME_INVALID,"):
                raise RuntimeError(
                    f"MLX90640 frame failed: {line}"
                )

            elif line.startswith("FRAME_START,"):
                parts = line.split(",")

                if len(parts) != 5:
                    raise ValueError(
                        f"Invalid frame header: {line}"
                    )

                index = int(parts[1])
                width = int(parts[2])
                height = int(parts[3])
                timestamp = int(parts[4])

                if width != WIDTH or height != HEIGHT:
                    raise ValueError(
                        "Unexpected thermal resolution"
                    )

                rows = []

                for _ in range(HEIGHT):
                    row_raw = ser.readline()

                    if not row_raw:
                        raise TimeoutError(
                            "Missing thermal row"
                        )

                    row = np.fromstring(
                        row_raw.decode(
                            "utf-8",
                            errors="strict"
                        ).strip(),
                        sep=","
                    )

                    if len(row) != WIDTH:
                        raise ValueError(
                            "Invalid thermal row length"
                        )

                    rows.append(row)

                end_line = ser.readline().decode(
                    "utf-8",
                    errors="strict"
                ).strip()

                if end_line != f"FRAME_END,{index}":
                    raise ValueError(
                        f"Invalid frame ending: {end_line}"
                    )

                frame = np.array(
                    rows,
                    dtype=np.float32
                )

                frames[index] = frame
                frame_timestamps[index] = timestamp

                print(
                    f"MLX90640: {len(frames)}/{FRAME_COUNT}"
                )

        if not completed:
            raise TimeoutError(
                "Calibration did not reach CAL_END"
            )

    # ======================================
    # VALIDATE COMPLETE CAPTURE
    # ======================================

    if len(sht_samples) != SHT_COUNT:
        raise RuntimeError(
            f"Expected {SHT_COUNT} SHT45 samples, "
            f"received {len(sht_samples)}"
        )

    if sorted(frames) != list(range(FRAME_COUNT)):
        raise RuntimeError(
            "Incomplete or duplicate thermal frames"
        )

    thermal_frames = np.stack(
        [frames[i] for i in range(FRAME_COUNT)]
    )

    if not np.isfinite(thermal_frames).all():
        raise RuntimeError(
            "Thermal frames contain invalid values"
        )

    metadata["capture_completed_at"] = (
        datetime.now(timezone.utc).isoformat()
    )
    metadata["frame_timestamps_ms"] = [
        frame_timestamps[i]
        for i in range(FRAME_COUNT)
    ]

    return sht_samples, thermal_frames, metadata


# ==========================================
# SAVE CALIBRATION RESULTS
# ==========================================

def save_results(samples, frames, metadata):
    folder = next_point_folder()

    # SHT45 individual samples
    with open(
        folder / "sht45_samples.csv",
        "w",
        newline="",
        encoding="utf-8"
    ) as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "sample",
                "uptime_ms",
                "temperature_c",
                "humidity_rh"
            ]
        )
        writer.writeheader()
        writer.writerows(samples)

    temperatures = np.array([
        s["temperature_c"] for s in samples
    ])

    humidity = np.array([
        s["humidity_rh"] for s in samples
    ])

    summary = {
        "temperature_c": {
            "mean": float(np.mean(temperatures)),
            "median": float(np.median(temperatures)),
            "std": float(np.std(temperatures, ddof=1))
        },
        "humidity_rh": {
            "mean": float(np.mean(humidity)),
            "median": float(np.median(humidity)),
            "std": float(np.std(humidity, ddof=1))
        }
    }

    (folder / "sht45_summary.json").write_text(
        json.dumps(summary, indent=2),
        encoding="utf-8"
    )

    # Save all 10 original thermal frames
    np.save(
        folder / "mlx90640_frames.npy",
        frames
    )

    # Save the averaged thermal matrix
    mean_frame = np.mean(frames, axis=0)

    np.savetxt(
        folder / "mlx90640_mean.csv",
        mean_frame,
        delimiter=",",
        fmt="%.4f"
    )

    # Apply display orientation only to the image
    display_frame = np.rot90(
        mean_frame,
        k=ROTATION
    )

    if FLIP_HORIZONTAL:
        display_frame = np.fliplr(display_frame)

    fig, ax = plt.subplots(figsize=(8, 6))

    image = ax.imshow(
        display_frame,
        cmap="inferno",
        interpolation="nearest",
        origin="upper"
    )

    ax.set_title(
        f"MLX90640 Interleaved — {folder.name}"
    )

    ax.set_xlabel("Pixel column")
    ax.set_ylabel("Pixel row")

    fig.colorbar(
        image,
        ax=ax,
        label="Temperature (°C)"
    )

    fig.tight_layout()

    fig.savefig(
        folder / "thermal_interleaved.png",
        dpi=200
    )

    plt.close(fig)

    metadata.update({
        "sht45_sample_count": len(samples),
        "mlx90640_frame_count": len(frames),
        "thermal_resolution": [HEIGHT, WIDTH],
        "rotation_k": ROTATION,
        "flip_horizontal": FLIP_HORIZONTAL,
        "image_interpolation": "nearest"
    })

    (folder / "metadata.json").write_text(
        json.dumps(metadata, indent=2),
        encoding="utf-8"
    )

    print("\nCALIBRATION SAVED")
    print("Folder:", folder)
    print(
        "Mean temperature:",
        round(summary["temperature_c"]["mean"], 3),
        "°C"
    )
    print(
        "Mean humidity:",
        round(summary["humidity_rh"]["mean"], 3),
        "% RH"
    )


# ==========================================
# MAIN
# ==========================================

if __name__ == "__main__":
    try:
        samples, frames, metadata = (
            capture_from_esp32()
        )

        save_results(
            samples,
            frames,
            metadata
        )

    except (
        serial.SerialException,
        TimeoutError,
        ValueError,
        RuntimeError
    ) as error:
        print("\nCALIBRATION FAILED:", error)
        print("No new calibration point was saved.")
