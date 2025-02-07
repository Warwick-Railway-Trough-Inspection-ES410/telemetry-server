import socketio
import time
import json

sio = socketio.Client()

@sio.on('connect')
def connected():
    print("Trough Inspection Robot Connected")

@sio.on('disconnect')
def disconnected():
    print("Client Disconnected")

sio.connect('http://localhost:5000', transports=['websocket'])

sio.emit("data_receive", {"message": "testing ..."})
sio.wait()
