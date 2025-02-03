import asyncio
import json
import time
from websockets.asyncio.client import connect

async def advertise(websocket):
    advert = {
        "type": "chan_id",
        "topic": "example_msg",
        "encoding": "json",
        "schemaName": "ExampleMsg",
        "schema": json.dumps(
            {
                "type": "object",
                "properties": {
                    "msg": {"type": "string"},
                    "count": {"type": "number"},
                },
            }
        ),
        "schemaEncoding": "jsonschema",
    }

#async def send_data(websocket):
#    while True:
#        await websocket.send(json.dumps(
#                {
#                    "message":"Hello",
#                    "count": 1,
 #           }))
#        await asyncio.sleep(1)

if __name__ == "__main__":
    async def start():
        uri = "ws://localhost:8765"
        async with connect(uri) as websocket:
            await advertise(websocket)
  #          await send_data(websocket)