
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

# -----------------------------------
# Configuration
# -----------------------------------

BASE_DIR = Path(__file__).resolve().parent
INPUT_FILE = BASE_DIR / "thermal_frames.txt"
OUTPUT_DIR = BASE_DIR / "analysis"
OUTPUT_DIR.mkdir(exist_ok=True)

WIDTH = 32
HEIGHT = 24


# -----------------------------------
# 1. Read thermal frames
# -----------------------------------

def load_frames(file_path):
    frames = []
    current_rows = []
    collecting = False
    frame_id = None

    with open(file_path, "r", encoding="utf-8") as file:
        for raw_line in file:
            line = raw_line.strip()

            if line.startswith("FRAME_START,"):
                parts = line.split(",")
                frame_id = int(parts[1])
                current_rows = []
                collecting = True
                continue

            if line.startswith("FRAME_END,"):
                if collecting:
                    frame = np.array(
                        current_rows, dtype=float
                    )

                    if frame.shape != (HEIGHT, WIDTH):
                        raise ValueError(
                            f"Frame {frame_id}: "
                            f"Expected {(HEIGHT, WIDTH)}, "
                            f"got {frame.shape}"
                        )

                    frames.append(frame)

                collecting = False
                continue

            if collecting:
                try:
                    values = [
                        float(x) for x in line.split(",")
                    ]
                except ValueError:
                    continue

                if len(values) == WIDTH:
                    current_rows.append(values)

    return np.array(frames)


# -----------------------------------
# 2. Generate heatmap
# -----------------------------------

def save_heatmap(data, title, filename,
                 cmap="inferno", vmin=None, vmax=None):

    plt.figure(figsize=(9, 6))

    image = plt.imshow(
        data,
        cmap=cmap,
        interpolation="nearest",
        origin="upper",
        vmin=vmin,
        vmax=vmax
    )

    plt.colorbar(image, label="Temperature (°C)")
    plt.title(title)
    plt.xlabel("Pixel column")
    plt.ylabel("Pixel row")

    plt.tight_layout()
    plt.savefig(
        OUTPUT_DIR / filename,
        dpi=200
    )
    plt.close()


# -----------------------------------
# 3. Main analysis
# -----------------------------------

def main():
    frames = load_frames(INPUT_FILE)

    print(f"Frames loaded: {len(frames)}")
    print(f"Frame shape: {frames.shape}")

    if len(frames) < 2:
        raise ValueError(
            "At least two frames are required."
        )

    # Per-pixel statistics
    mean_frame = np.mean(frames, axis=0)
    std_frame = np.std(frames, axis=0, ddof=1)

    # Global colour scale for comparisons
    vmin = np.min(frames)
    vmax = np.max(frames)

    # Save individual frames
    for i, frame in enumerate(frames, start=1):
        np.savetxt(
            OUTPUT_DIR / f"frame_{i}.csv",
            frame,
            delimiter=",",
            fmt="%.2f"
        )

        save_heatmap(
            frame,
            f"MLX90640 Thermal Frame {i}",
            f"frame_{i}.png",
            vmin=vmin,
            vmax=vmax
        )

    # Save mean heatmap
    np.savetxt(
        OUTPUT_DIR / "mean_frame.csv",
        mean_frame,
        delimiter=",",
        fmt="%.4f"
    )

    save_heatmap(
        mean_frame,
        "MLX90640 Mean Temperature Heatmap",
        "mean_heatmap.png",
        vmin=vmin,
        vmax=vmax
    )

    # Save standard deviation heatmap
    np.savetxt(
        OUTPUT_DIR / "std_frame.csv",
        std_frame,
        delimiter=",",
        fmt="%.4f"
    )

    save_heatmap(
        std_frame,
        "MLX90640 Pixel Standard Deviation",
        "std_heatmap.png",
        cmap="viridis"
    )

    # Frame-to-frame differences
    for i in range(len(frames) - 1):
        difference = frames[i + 1] - frames[i]

        np.savetxt(
            OUTPUT_DIR / f"difference_{i+1}_{i+2}.csv",
            difference,
            delimiter=",",
            fmt="%.4f"
        )

        save_heatmap(
            difference,
            f"Frame {i+2} - Frame {i+1}",
            f"difference_{i+1}_{i+2}.png",
            cmap="coolwarm",
            vmin=-max(abs(difference.min()),
                      abs(difference.max())),
            vmax=max(abs(difference.min()),
                     abs(difference.max()))
        )

    # Print summary
    print("\n--- ANALYSIS RESULTS ---")

    print(f"Mean temperature: "
          f"{np.mean(mean_frame):.3f} °C")

    print(f"Minimum temperature: "
          f"{np.min(frames):.3f} °C")

    print(f"Maximum temperature: "
          f"{np.max(frames):.3f} °C")

    print(f"Mean pixel std deviation: "
          f"{np.mean(std_frame):.4f} °C")

    print(f"Maximum pixel std deviation: "
          f"{np.max(std_frame):.4f} °C")

    print("\nAnalysis saved to:")
    print(OUTPUT_DIR)


if __name__ == "__main__":
    main()
