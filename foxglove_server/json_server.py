import asyncio
import json
import time
from datetime import datetime
import time

from foxglove_websocket import run_cancellable
from foxglove_websocket.server import FoxgloveServer, FoxgloveServerListener
from foxglove_websocket.types import (
    ChannelId,
    ClientChannel,
    ClientChannelId,
    ServiceId,
)

# Load any JSON schemas we will use
with open('foxglove_server/jsonschema/GeoJSON.json', 'r') as file:
    GeoJSON_schema = file.read()
with open('foxglove_server/jsonschema/LocationFix.json', 'r') as file:
    LocationFix_schema = file.read()
with open('foxglove_server/jsonschema/CompressedImage.json', 'r') as file:
    CompressedImage_schema = file.read()
with open('foxglove_server/jsonschema/Log.json', 'r') as file:
    Log_schema = file.read()

async def main(message_queue, loop):

    class Listener(FoxgloveServerListener):
        async def on_subscribe(self, server: FoxgloveServer, channel_id: ChannelId):
            print("First client subscribed to", channel_id)

        async def on_unsubscribe(self, server: FoxgloveServer, channel_id: ChannelId):
            print("Last client unsubscribed from", channel_id)

        async def on_client_advertise(
            self, server: FoxgloveServer, channel: ClientChannel
        ):
            print("Client advertise:", json.dumps(channel))

        async def on_client_unadvertise(
            self, server: FoxgloveServer, channel_id: ClientChannelId
        ):
            print("Client unadvertise:", channel_id)

        async def on_client_message(
            self, server: FoxgloveServer, channel_id: ClientChannelId, payload: bytes
        ):
            msg = json.loads(payload)
            print(f"Client message on channel {channel_id}: {msg}")

        async def on_service_request(
            self,
            server: FoxgloveServer,
            service_id: ServiceId,
            call_id: str,
            encoding: str,
            payload: bytes,
        ) -> bytes:
            if encoding != "json":
                return json.dumps(
                    {"success": False, "error": f"Invalid encoding {encoding}"}
                ).encode()

            request = json.loads(payload)
            if "data" not in request:
                return json.dumps(
                    {"success": False, "error": f"Missing key 'data'"}
                ).encode()

            print(f"Service request on service {service_id}: {request}")
            return json.dumps(
                {"success": True, "message": f"Received boolean: {request['data']}"}
            ).encode()

    async with FoxgloveServer(
        "0.0.0.0",
        8765,
        "example server",
        capabilities=["clientPublish", "services"],
        supported_encodings=["json"],
    ) as server:
        server.set_listener(Listener())
        geo_chan = await server.add_channel(
            {
                "topic": "MapAnnotation",
                "encoding": "json",
                "schemaName": "foxglove.GeoJSON",
                "schema": GeoJSON_schema,
                "schemaEncoding": "jsonschema",
            }
        )
        location_chan = await server.add_channel(
            {
                "topic": "GPS",
                "encoding": "json",
                "schemaName": "foxglove.LocationFix",
                "schema": LocationFix_schema,
                "schemaEncoding": "jsonschema",
            }
        )
        cam1_chan = await server.add_channel(
            {
                "topic": "Camera1",
                "encoding": "json",
                "schemaName": "foxglove.CompressedImage",
                "schema": CompressedImage_schema,
                "schemaEncoding": "jsonschema",
            }
        )
        cam2_chan = await server.add_channel(
            {
                "topic": "Camera2",
                "encoding": "json",
                "schemaName": "foxglove.CompressedImage",
                "schema": CompressedImage_schema,
                "schemaEncoding": "jsonschema",
            }
        )
        log_chan = await server.add_channel(
            {
                "topic": "Log Message",
                "encoding": "json",
                "schemaName": "foxglove.Log",
                "schema": Log_schema,
                "schemaEncoding": "jsonschema",
            }
        )

        while True:
            message = await message_queue.get()
            print(f"Sending message to Foxglove: {message[0]}")
            if message[0] == 'log':
                payload = await handle_log(message) 
                await server.send_message(
                    log_chan,
                    time.time_ns(),
                    payload,
                )  
            elif message[0] == 'status':
                payload = await handle_status(message) 

                await server.send_message(
                    location_chan,
                    time.time_ns(),
                    payload,
                )  
            elif message[0] == 'trough_status':
                payload = await handle_trough_status(message) 

                # await server.send_message(
                #     log_chan,
                #     time.time_ns(),
                #     payload,
                # )  
            elif message[0] == 'trough_feature':
                payload = await handle_trough_feature(message) 

                await server.send_message(
                    cam1_chan,
                    time.time_ns(),
                    payload,
                )  
            else:
                print("Cannot send to Foxglove, unknown message time (check Flask endpoint)")

async def handle_status(message):
    latitude = message[1]["gps"]["latitude"]
    longitude = message[1]["gps"]["longitude"]
    altitude = message[1]["gps"]["longitude"]
    timestamp = message[1]["timestamp"] 
    dt = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S.%f+00:00Z")
    epoch_seconds = dt.timestamp()

    payload = json.dumps({
        "timestamp": {
            "sec": epoch_seconds,
            "nsec": 0
        },
        "frame_id": "abc",
        "latitude": latitude,
        "longitude": longitude,
        "altitude": longitude,
        "position_covariance": [0.1, 0.0, 0.0, 0.0, 0.1, 0.0, 0.0, 0.0, 0.1],
        "position_covariance_type": 2
        }).encode("utf8")
    return payload

async def handle_log(message):
    level = message[1]["level"]
    log_message_text = message[1]["message"] 
    timestamp = message[1]["timestamp"] 
    dt = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S.%f+00:00Z")
    epoch_seconds = dt.timestamp()

    payload = json.dumps({
        "timestamp": {
            "sec": epoch_seconds,
            "nsec": 0
        },
        "level": level,
        "message": log_message_text,
        "name": "Flask",
        "file": "test",
        "line": 0
        }).encode("utf8")
    return payload

async def handle_trough_status(message):
    pass

async def handle_trough_feature(message):
    image_data = message[1]["data"]
    timestamp = message[1]["timestamp"] 
    dt = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S.%f+00:00Z")
    epoch_seconds = int(dt.timestamp())

    payload = json.dumps({
        "timestamp": {
            "sec": epoch_seconds,
            "nsec": 0
        },
        "frame_id": "abc",
        "data": image_data,
        "format": "jpg"
        }).encode("utf8")
    return payload

# Called externally to start Foxglove server
async def run(message_queue, loop):
    print("Starting Foxglove thread")
    await main(message_queue, loop)
    
if __name__ == "__main__":
    run(None, None)