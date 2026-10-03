import serial
import json

SERIAL_PORT = "COM5"
BAUD_RATE = 115200

esp32 = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)

print("CDE4301 Gateway")
print(f"Listening to {SERIAL_PORT}...")

while True:
    line = esp32.readline().decode("utf-8").strip()

    if not line:
        continue

    try:
        data = json.loads(line)

        print(
            f"Node: {data['node_id']} | "
            f"Sensor: {data['sensor']} | "
            f"Temperature: {data['temperature_c']} °C"
        )

    except json.JSONDecodeError:
        # Ignore ESP32 boot messages and other non-JSON output
        pass