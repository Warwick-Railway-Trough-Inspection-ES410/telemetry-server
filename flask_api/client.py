import socketio
from datetime import datetime, timezone
import json

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

data =  {
    "level": 1,
    "message": "Test message...",
    "timestamp": iso_time
}
send_data("log", data)

sio.disconnect()
