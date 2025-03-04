import socketio
from datetime import datetime, timezone
import json
import time

sio = socketio.Client()

def send_data(endpoint, data):
    response = sio.call(endpoint, data)
    print(f"Response from {endpoint}: {response}")

@sio.on('connect')
def connected():
    print("Connected to server")

@sio.on('disconnect')
def disconnected():
    print("Disconnected from server")

sio.connect('http://localhost:3000', transports=['websocket'])

# Get current time in ISO 8601 format
iso_time = datetime.now(timezone.utc).isoformat() + "Z"

lat = 52.382768190299394
lon = -1.561584788207353

while True:
    try:
        data = {
            "status": 1,
            "battery": 85,
            "distance_travelled": 1203.5,
            "signal_quality": 75.2,
            "gps": {
                "latitude": lat,
                "longitude": lon,
                "altitude": 0
            },
            "imu": {
                "acceleration": [0.01, -0.02, 9.81],
                "gyro": [0.0, 0.05, -0.07]
            },
            "timestamp": iso_time
        }

        send_data("status", data)

        time.sleep(3)
        lat = lat + 1e-5
        lon = lon - 2e-5
    except KeyboardInterrupt:
        break

sio.disconnect()
