import asyncio
import json
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

async def main():
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
        await server.add_service(
            {
                "name": "example_set_bool",
                "request": {
                    "encoding": "json",
                    "schemaName": "requestSchema",
                    "schemaEncoding": "jsonschema",
                    "schema": json.dumps(
                        {
                            "type": "object",
                            "properties": {
                                "data": {"type": "boolean"},
                            },
                        }
                    ),
                },
                "response": {
                    "encoding": "json",
                    "schemaName": "responseSchema",
                    "schemaEncoding": "jsonschema",
                    "schema": json.dumps(
                        {
                            "type": "object",
                            "properties": {
                                "success": {"type": "boolean"},
                                "message": {"type": "string"},
                            },
                        }
                    ),
                },
                "requestSchema": None,
                "responseSchema": None,
                "type": "example_set_bool",
            }
        )

        i = 0
        while True:
            i += 1
            await asyncio.sleep(0.5)
            await server.send_message(
                log_chan,
                time.time_ns(),
                json.dumps({
                    "timestamp": {
                        "sec": 10000,
                        "nsec": 1000
                    },
                    "level": 0,
                    "message": "hello world",
                    "name": "idk",
                    "file": "test",
                    "line": 0
                }).encode("utf8"),
            )

def run():
    print("Starting Foxglove thread")
    run_cancellable(main())
    
if __name__ == "__main__":
    run()