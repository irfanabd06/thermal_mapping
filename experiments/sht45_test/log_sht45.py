
import csv
import serial
from pathlib import Path
from datetime import datetime

PORT = "COM7"
import csv
import time
from pathlib import Path
from datetime import datetime

import serial
from serial import SerialException

PORT = "COM7"
BAUD_RATE = 115200
TOTAL_SAMPLES = 30

OUTPUT_DIR = Path(__file__).resolve().parent
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

filename = (
    "sht45_"
    + datetime.now().strftime("%Y%m%d_%H%M%S")
    + ".csv"
)

output_file = OUTPUT_DIR / filename

print(f"Connecting to {PORT}...")

try:
    with serial.Serial(
        PORT,
        BAUD_RATE,
        timeout=1
    ) as ser:

        # Allow serial connection to settle
        time.sleep(2)

        # Clear old serial messages
        ser.reset_input_buffer()

        print("Sending START command...")

        ser.write(b"START\n")
        ser.flush()

        count = 0
        started = False
        last_data_time = time.monotonic()

        with open(
            output_file,
            "w",
            newline="",
            encoding="utf-8"
        ) as f:

            writer = csv.writer(f)

            writer.writerow([
                "sample",
                "elapsed_s",
                "temperature_c",
                "humidity_rh",
                "valid",
                "recorded_at"
            ])

            while count < TOTAL_SAMPLES:

                raw = ser.readline()

                if not raw:
                    if time.monotonic() - last_data_time > 45:
                        raise TimeoutError(
                            "No experiment data for 45 seconds."
                        )
                    continue

                line = raw.decode(
                    "utf-8",
                    errors="replace"
                ).strip()

                if line == "SHT45_EXPERIMENT_START":
                    started = True
                    print("Experiment started!")
                    last_data_time = time.monotonic()
                    continue

                if not line.startswith("DATA,"):
                    continue

                if not started:
                    print("Warning: received DATA before START marker.")
                    started = True

                parts = line.split(",")

                if len(parts) != 6:
                    print("Invalid row:", line)
                    continue

                _, sample, elapsed, temp, rh, valid = parts

                sample_num = int(sample)

                if sample_num != count + 1:
                    raise ValueError(
                        f"Unexpected sample number: {sample_num}"
                    )

                timestamp = datetime.now().astimezone().isoformat(
                    timespec="seconds"
                )

                writer.writerow([
                    sample_num,
                    elapsed,
                    temp,
                    rh,
                    valid,
                    timestamp
                ])

                f.flush()

                count += 1
                last_data_time = time.monotonic()

                print(
                    f"[{count}/{TOTAL_SAMPLES}] "
                    f"Time={elapsed}s | "
                    f"T={temp} C | RH={rh}% | "
                    f"Valid={valid}"
                )

        print("\nExperiment completed successfully!")

except (SerialException, TimeoutError, ValueError) as error:
    print(f"\nExperiment stopped: {error}")
    print("Check the USB connection and console settings.")

print(f"CSV location: {output_file}")

BAUD_RATE = 115200
TOTAL_SAMPLES = 30

output_dir = Path(__file__).resolve().parent
output_file = output_dir / "sht45_test.csv"

print(f"Connecting to {PORT}...")

with serial.Serial(PORT, BAUD_RATE, timeout=2) as ser:
    with open(output_file, "w", newline="") as f:
        writer = csv.writer(f)

        writer.writerow([
            "sample",
            "elapsed_s",
            "temperature_c",
            "humidity_rh",
            "valid",
            "recorded_at"
        ])

        print("Waiting for SHT45 measurements...")

        count = 0

        while count < TOTAL_SAMPLES:
            line = ser.readline().decode(
                "utf-8", errors="replace"
            ).strip()

            if not line.startswith("DATA,"):
                continue

            parts = line.split(",")

            if len(parts) != 6:
                continue

            _, sample, elapsed, temp, rh, valid = parts

            timestamp = datetime.now().isoformat(
                timespec="seconds"
            )

            writer.writerow([
                sample,
                elapsed,
                temp,
                rh,
                valid,
                timestamp
            ])

            f.flush()

            count += 1

            print(
                f"[{count}/{TOTAL_SAMPLES}] "
                f"T={temp} C | RH={rh}%"
            )

print(f"\nExperiment completed!")
print(f"CSV saved to: {output_file}")
