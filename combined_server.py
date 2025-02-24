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
import threading
import asyncio
import flask_api.app as flask_server
import foxglove_server.json_server as foxglove_server

def main_runner():
    flask_thread = threading.Thread(target=flask_server.run(), daemon=False)
    flask_thread.start()

    foxglove_server.run()


if __name__ == '__main__':
    main_runner()  # Start both servers