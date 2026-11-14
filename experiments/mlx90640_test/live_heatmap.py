
import serial
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import RectangleSelector

# ==========================================
# CONFIGURATION
# ==========================================

PORT = "COM7"
BAUD_RATE = 115200

WIDTH = 32
HEIGHT = 24

ROTATION = 1
FLIP_HORIZONTAL = True

TEMP_MIN = 25
TEMP_MAX = 40


def main():

    print(f"Connecting to {PORT}...")

    with serial.Serial(PORT, BAUD_RATE, timeout=0.05) as ser:

        plt.ion()

        fig, ax = plt.subplots(figsize=(9, 6))

        # Initial image (display dimensions)
        initial_frame = np.full(
            (HEIGHT, WIDTH),
            30.0
        )

        initial_frame = np.rot90(
            initial_frame,
            k=ROTATION
        )

        if FLIP_HORIZONTAL:
            initial_frame = np.fliplr(initial_frame)

        display_height, display_width = initial_frame.shape

        image = ax.imshow(
            initial_frame,
            cmap="inferno",
            interpolation="bilinear",
            origin="upper",
            vmin=TEMP_MIN,
            vmax=TEMP_MAX
        )

        plt.colorbar(
            image,
            ax=ax,
            label="Temperature (°C)"
        )

        ax.set_xlabel("Pixel column")
        ax.set_ylabel("Pixel row")
        ax.set_title("Waiting for MLX90640 frames...")

        # ==================================
        # CENTRE CROSSHAIR
        # ==================================

        ax.axvline(
            (display_width - 1) / 2,
            color="cyan",
            linewidth=2,
            linestyle="--"
        )

        ax.axhline(
            (display_height - 1) / 2,
            color="cyan",
            linewidth=2,
            linestyle="--"
        )

        # ==================================
        # ROI SELECTION
        # ==================================

        roi = {"coords": None}

        def on_select(eclick, erelease):

            if eclick.xdata is None or erelease.xdata is None:
                return

            x1, x2 = sorted([
                eclick.xdata,
                erelease.xdata
            ])

            y1, y2 = sorted([
                eclick.ydata,
                erelease.ydata
            ])

            roi["coords"] = (x1, y1, x2, y2)

            print(
                f"ROI selected: {roi['coords']}"
            )

        selector = RectangleSelector(
            ax,
            on_select,
            useblit=False,
            button=[1],
            minspanx=1,
            minspany=1,
            spancoords="data",
            interactive=True,
            props=dict(
                edgecolor="lime",
                facecolor="none",
                linewidth=3,
                linestyle="-"
            )
        )

        # ==================================
        # INTERPOLATION SWITCH
        # ==================================

        def on_key(event):

            if event.key == "n":
                image.set_interpolation("nearest")
                print("Interpolation: nearest")

            elif event.key == "b":
                image.set_interpolation("bilinear")
                print("Interpolation: bilinear")

            fig.canvas.draw_idle()

        fig.canvas.mpl_connect(
            "key_press_event",
            on_key
        )

        plt.show(block=False)

        # ==================================
        # SERIAL FRAME RECEPTION
        # ==================================

        collecting = False
        rows = []
        frame_count = 0

        print("Waiting for thermal frames...")

        while plt.fignum_exists(fig.number):

            # Keep GUI responsive
            plt.pause(0.01)

            raw = ser.readline()

            if not raw:
                continue

            line = raw.decode(
                "utf-8",
                errors="replace"
            ).strip()

            # Start of frame
            if line.startswith("FRAME_START,"):

                collecting = True
                rows = []

                continue

            if not collecting:
                continue

            # End of frame
            if line.startswith("FRAME_END,"):

                if len(rows) == HEIGHT:

                    thermal_frame = np.array(
                        rows,
                        dtype=float
                    )

                    # Rotate and flip
                    display_frame = np.rot90(
                        thermal_frame,
                        k=ROTATION
                    )

                    if FLIP_HORIZONTAL:
                        display_frame = np.fliplr(
                            display_frame
                        )

                    # Update heatmap
                    image.set_data(display_frame)

                    frame_count += 1

                    # Centre temperature
                    h, w = display_frame.shape

                    center_row = h // 2
                    center_col = w // 2

                    center_temp = display_frame[
                        center_row,
                        center_col
                    ]

                    # ==================================
                    # ROI TEMPERATURE STATISTICS
                    # ==================================

                    roi_text = ""

                    if roi["coords"] is not None:

                        x1, y1, x2, y2 = roi["coords"]

                        col_start = max(
                            0, int(np.ceil(x1))
                        )

                        col_end = min(
                            w, int(np.floor(x2)) + 1
                        )

                        row_start = max(
                            0, int(np.ceil(y1))
                        )

                        row_end = min(
                            h, int(np.floor(y2)) + 1
                        )

                        selected = display_frame[
                            row_start:row_end,
                            col_start:col_end
                        ]

                        if selected.size > 0:

                            roi_text = (
                                f"\nROI Mean: "
                                f"{np.mean(selected):.2f}°C | "
                                f"Median: "
                                f"{np.median(selected):.2f}°C"
                            )

                    # Single title update
                    ax.set_title(
                        "MLX90640 Live Thermal Camera\n"
                        f"Center: {center_temp:.2f}°C | "
                        f"Min: {display_frame.min():.2f}°C | "
                        f"Max: {display_frame.max():.2f}°C"
                        + roi_text
                    )

                    fig.canvas.draw_idle()

                    if frame_count % 10 == 0:
                        print(
                            f"Received {frame_count} frames"
                        )

                else:
                    print(
                        f"Incomplete frame: "
                        f"{len(rows)}/{HEIGHT} rows"
                    )

                collecting = False
                continue

            # Read temperature row
            try:

                values = [
                    float(x)
                    for x in line.split(",")
                ]

                if len(values) == WIDTH:
                    rows.append(values)

            except ValueError:
                continue

        plt.ioff()


if __name__ == "__main__":
    main()
