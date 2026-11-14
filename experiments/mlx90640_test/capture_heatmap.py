
import csv
from datetime import datetime
from pathlib import Path

import serial
import numpy as np
import matplotlib.pyplot as plt

# Configuration
PORT = "COM7"
BAUD_RATE = 115200
WIDTH = 32
HEIGHT = 24

OUTPUT_DIR = Path(__file__).resolve().parent
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def capture_frame():
    print(f"Connecting to ESP32-C6 on {PORT}...")

    with serial.Serial(PORT, BAUD_RATE, timeout=2) as ser:
        print("Waiting for thermal frame...")

        collecting = False
        rows = []

        while True:
            raw = ser.readline()
            line = raw.decode(
                "utf-8", errors="replace"
            ).strip()

            if line:
                print("ESP32:", line)

            if line.startswith("FRAME_START,"):
                collecting = True
                rows = []
                print("Receiving thermal frame...")
                continue

            if not collecting:
                continue

            if line.startswith("FRAME_END,"):
                if len(rows) != HEIGHT:
                    raise ValueError(
                        f"Expected {HEIGHT} rows, got {len(rows)}"
                    )

                return np.array(rows, dtype=float)

            try:
                values = [float(x) for x in line.split(",")]
            except ValueError:
                continue

            if len(values) == WIDTH:
                rows.append(values)


def save_frame(frame):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    csv_path = OUTPUT_DIR / f"mlx90640_{timestamp}.csv"
    png_path = OUTPUT_DIR / f"mlx90640_{timestamp}.png"

    # 1. Save original temperature measurements
    np.savetxt(
        csv_path,
        frame,
        delimiter=",",
        fmt="%.2f"
    )

    # 2. Select a region containing the leaf
    # Example only: rows 8-15, columns 10-19
    leaf_region = frame[8:16, 10:20]

    # 3. Calculate leaf temperature statistics
    leaf_mean = np.mean(leaf_region)
    leaf_median = np.median(leaf_region)

    print(f"Leaf region mean: {leaf_mean:.2f} °C")
    print(f"Leaf region median: {leaf_median:.2f} °C")

    # 4. Display using bilinear interpolation
    plt.figure(figsize=(9, 6))

    image = plt.imshow(
        frame,
        cmap="inferno",
        interpolation="bilinear",
        origin="upper"
    )

    plt.colorbar(image, label="Temperature (°C)")
    plt.title("MLX90640-BAB Leaf Temperature")
    plt.xlabel("Pixel column")
    plt.ylabel("Pixel row")

    plt.tight_layout()
    plt.savefig(png_path, dpi=200)

    print(f"CSV saved: {csv_path}")
    print(f"Heatmap saved: {png_path}")

    plt.show()


if __name__ == "__main__":
    thermal_frame = capture_frame()

    print("Frame shape:", thermal_frame.shape)
    print("Minimum:", np.min(thermal_frame))
    print("Maximum:", np.max(thermal_frame))
    print("Average:", np.mean(thermal_frame))

    save_frame(thermal_frame)
