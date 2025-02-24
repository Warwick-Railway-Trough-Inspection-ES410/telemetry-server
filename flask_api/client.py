import socketio
import time
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

data =  {
    "level": 1,
    "message": "Test message...",
    "timestamp": "2025-02-24T09:00:00.123Z"
}
send_data("log", data)

sio.wait()
