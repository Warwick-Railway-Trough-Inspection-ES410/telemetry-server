import socketio
from datetime import datetime, timezone
import json
import time
import base64

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

image_path = "test_image.jpg"  # Change to your image file path

def image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode("utf-8")
    return encoded_string

image_data = image_to_base64(image_path)

while True:
    try:
        data = {
            "feature_type": 0,
            "gps": {
                "latitude": lat,
                "longitude": lon,
                "altitude": 0
            },
            "timestamp": iso_time,
            "data": image_data
        }

        send_data("trough_feature", data)

        time.sleep(20)
    except KeyboardInterrupt:
        break

sio.disconnect()
