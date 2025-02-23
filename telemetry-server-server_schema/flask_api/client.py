import socketio
import time
import json

sio = socketio.Client()
sio.connect('http://localhost:3000?token=AJHKBCBS^&"VDPANIB"*BJA', transports=['websocket'], headers={'token': 'AJHKBCBS^&"VDPANIB"*BJA'}) #Only one of token things is needed but not sure which
@sio.on('connect')
def connected():
    print("Trough Inspection Robot Connected")

@sio.on('disconnect')
def disconnected():
    print("Client Disconnected")

#Random data of correct format:
geojson_object = {
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Example",
            "geometry": {
                "type": "ExamplePoint",
                "coordinates": [12, 0.1]
            },
            "properties": {
                "name": "FirstPoint"
            }
        }
    ]
}
geojson_str = json.dumps(geojson_object)
#Formatting:
data_to_send = {
    "geojson": geojson_str  
}
sio.emit("data_receive", data_to_send) #Sending example data to Flask server

sio.wait()
