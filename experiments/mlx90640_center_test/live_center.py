
import time
import serial
import numpy as np
import matplotlib.pyplot as plt

# ==========================================
# CONFIGURATION
# ==========================================

PORT = "COM7"
BAUD_RATE = 115200

WIDTH = 32
HEIGHT = 24

# Camera orientation
ROTATION = 1
FLIP_HORIZONTAL = False

# Display settings
AUTO_SCALE = True
FIXED_MIN = 25.0
FIXED_MAX = 50.0

# Limit plot redraws to avoid unnecessary work
DISPLAY_FPS = 15

# ==========================================
# IMAGE ORIENTATION
# ==========================================

def orient_frame(frame):
    frame = np.rot90(frame, k=ROTATION)

    if FLIP_HORIZONTAL:
        frame = np.fliplr(frame)

    return frame


# ==========================================
# READ ONE COMPLETE FRAME
# ==========================================

def read_frame(ser):
    # Find start marker
    while True:
        line = ser.readline().decode(
            "utf-8",
            errors="replace"
        ).strip()

        if line == "FRAME_START":
            break

        if not line:
            return None

    rows = []

    for _ in range(HEIGHT):
        line = ser.readline().decode(
            "utf-8",
            errors="replace"
        ).strip()

        try:
            values = np.array(
                [
                    float(value)
                    for value in line.split(",")
                ],
                dtype=np.float32
            )
        except ValueError:
            return None

        if values.size != WIDTH:
            return None

        rows.append(values)

    ending = ser.readline().decode(
        "utf-8",
        errors="replace"
    ).strip()

    if ending != "FRAME_END":
        return None

    return np.stack(rows)


# ==========================================
# MAIN
# ==========================================

def main():

    print(f"Connecting to ESP32-C6 on {PORT}...")

    with serial.Serial(
        PORT,
        BAUD_RATE,
        timeout=0.3
    ) as ser:

        print("Waiting for thermal frames...")

        plt.ion()

        fig, ax = plt.subplots(figsize=(8, 7))

        initial = np.zeros((WIDTH, HEIGHT))

        image = ax.imshow(
            initial,
            cmap="inferno",
            interpolation="nearest",
            origin="upper",
            vmin=FIXED_MIN,
            vmax=FIXED_MAX
        )

        colorbar = fig.colorbar(
            image,
            ax=ax,
            label="Temperature (°C)"
        )

        ax.set_xlabel("Pixel column")
        ax.set_ylabel("Pixel row")

        h, w = initial.shape

        center_x = (w - 1) / 2
        center_y = (h - 1) / 2

        ax.axvline(
            center_x,
            color="cyan",
            linestyle="--",
            linewidth=1
        )

        ax.axhline(
            center_y,
            color="cyan",
            linestyle="--",
            linewidth=1
        )

        last_draw = 0.0
        last_frame_time = None
        fps = 0.0

        # ==================================
        # LIVE LOOP
        # ==================================

        while plt.fignum_exists(fig.number):

            raw_frame = read_frame(ser)

            if raw_frame is None:
                plt.pause(0.001)
                continue

            frame = orient_frame(raw_frame)

            now = time.monotonic()

            # Calculate received frame rate
            if last_frame_time is not None:
                dt = now - last_frame_time

                if dt > 0:
                    instantaneous_fps = 1.0 / dt

                    fps = (
                        0.8 * fps
                        + 0.2 * instantaneous_fps
                    )

            last_frame_time = now

            # Avoid excessive redraws
            if now - last_draw < 1.0 / DISPLAY_FPS:
                continue

            last_draw = now

            image.set_data(frame)

            valid = frame[np.isfinite(frame)]

            if valid.size == 0:
                continue

            temp_min = float(np.min(valid))
            temp_max = float(np.max(valid))

            # Automatic colour scaling
            if AUTO_SCALE:
                lower = temp_min - 0.5
                upper = temp_max + 0.5

                if upper > lower:
                    image.set_clim(
                        vmin=lower,
                        vmax=upper
                    )

            # Centre 2x2 measurement
            height, width = frame.shape

            center_region = frame[
                height // 2 - 1:height // 2 + 1,
                width // 2 - 1:width // 2 + 1
            ]

            center_temp = float(
                np.nanmean(center_region)
            )

            ax.set_title(
                "MLX90640 Live Thermal Camera\n"
                f"Center: {center_temp:.2f}°C | "
                f"Min: {temp_min:.2f}°C | "
                f"Max: {temp_max:.2f}°C | "
                f"FPS: {fps:.1f}"
            )

            fig.canvas.draw_idle()
            plt.pause(0.001)

        plt.close(fig)


if __name__ == "__main__":
    try:
        main()

    except KeyboardInterrupt:
        print("\nLive viewer stopped.")

    except serial.SerialException as error:
        print("Serial error:", error)
