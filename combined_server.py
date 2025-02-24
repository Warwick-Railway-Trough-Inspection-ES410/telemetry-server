"""
combined_server.py
==================

Integrates the Flask and Foxglove-websocket servers into one application
Author(s): Chris Taylor, Harry Upton

Implementation Notes
--------------------
- The Flask server is run in a separate thread
- The Foxglove server uses asyncio
- flask_api/schema/... contains JSON schemas for communication between the robot and Flask server
- foxglove_server/jsonschema and foxglove_server/customschema contain JSON schemas for communication 
 between the Foxglove server (this) and Foxglove client (GUI)

Missing Features (ToDo):
------------------------

"""
import flask_api.app as flask_server
import foxglove_server.json_server as foxglove_server
import asyncio
import threading


async def main_runner():
    message_queue = asyncio.Queue()
    loop = asyncio.get_running_loop()

    flask_thread = threading.Thread(target=flask_server.run, args=(message_queue, loop), daemon=True)
    flask_thread.start()

    await foxglove_server.run(message_queue, loop)


if __name__ == '__main__':
    asyncio.run(main_runner()) # Start both servers