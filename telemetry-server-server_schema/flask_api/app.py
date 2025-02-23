from flask import Flask, request, jsonify, render_template
from flask_socketio import SocketIO, emit
import websockets

from foxglove_websocket import run_cancellable
from foxglove_websocket.server import FoxgloveServer, FoxgloveServerListener
from foxglove_websocket.types import ChannelId, ClientChannel
import asyncio
import time
import json
#Import Schema
with open('C:/Users/chris/PythonFun/WebApp_Files/venv/Scripts/telemetry-server-server_schema/foxglove_server/jsonschema/GeoJSON.json', 'r') as file: 
    GeoJSON_schema = file.read()

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins=["http://localhost:3000", "http://127.0.0.1:3000"]) #Change for production!
foxglove = "ws://127.0.0.1:8765" #Foxglove address

#Send message received from client to Foxglove:
async def send_to_foxglove(data):
    await asyncio.sleep(2) #Allow time for Foxglove server just in case
    async with websockets.connect(foxglove) as websocket:
        
        geo_chan = {
            "topic": "MapAnnotation",
            "encoding": "json",
            "schemaName": "foxglove.GeoJSON",
            "schema": GeoJSON_schema,
            "schemaEncoding": "jsonschema",
        }
            
        message = {
            "op": 0x02, #PROBLEM!
            "channel": geo_chan,
            "data": data
        }
        await websocket.send(json.dumps(message)) #.encode("utf8")
        print(f"Sending to Foxglove server: {data}")
        while True:
            await asyncio.sleep(10)  #Keep open

#Receiving data from client:    
@socketio.on('data_receive')
def handle_json(json):
    if not isinstance(json, dict) or 'geojson' not in json:
        print("Invalid data format received.")
        return
    print('Received json:', json)
    asyncio.run(send_to_foxglove(json)) #Call function to send on message to Foxglove

#Allow client to connect and send data:
@socketio.on('connect')
def test_connect(message):
    token = request.headers.get('token')
    if token != 'AJHKBCBS^&"VDPANIB"*BJA': #Little bit of security
        print("Unauthorized connection attempt!")
        return False
    print("Success:", message)
    emit("Successfully received")

@socketio.on('disconnect')
def test_disconnect(reason):
    print('Client disconnected, reason:', reason)

#Redundant at this point but this is what appears on the actual webpage
@app.route("/")
def formatted_data ():
    formatted_data = {
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
    }
    return jsonify(formatted_data)

if __name__ == '__main__':
    #socketio.run(app, port=3000, debug=True)
    socketio.run(app, host="127.0.0.1", port=3000, debug=False)