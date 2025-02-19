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

sio.connect('http://localhost:3000', transports=['websocket'])

#sio.emit("data_receive", {"message": "testing ..."})
sio.emit("data_receive", {
        'position': ["1.0000", "1.0000", "1.0000"],
        'status': 1,
        'battery': 100,
        'dist_trav': 10,
        #Signal quality - if required
        'IMU': ["1.0000", "1.0000", "1.0000"],
        'trough':
            {
            'nCables': 5.0000,
            'areaCables': 80.0000,
            },
        'image': "ABC+=/akla+-" #Base 64 Image 
    })
sio.wait()
