
import serial
from datetime import datetime

SERIAL_PORT = "/dev/ttyUSB0"
BAUD_RATE = 9600

def main():
    print(f"Listening for RS-485 data on {SERIAL_PORT}")

    with serial.Serial(
        SERIAL_PORT,
        BAUD_RATE,
        timeout=1
    ) as port:

        while True:
            raw = port.readline()

            if not raw:
                continue

            message = raw.decode(
                "utf-8",
                errors="replace"
            ).strip()

            if message:
                timestamp = datetime.now().astimezone().isoformat(
                    timespec="seconds"
                )

                print(
                    f"[{timestamp}] Received: {message}",
                    flush=True
                )

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nReceiver stopped.")
    except serial.SerialException as error:
        print(f"Serial error: {error}")
