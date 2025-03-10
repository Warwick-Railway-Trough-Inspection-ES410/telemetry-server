from flask import Flask
from flask_socketio import SocketIO, emit
import json
from jsonschema import validate, ValidationError
import asyncio

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins='*') #Change for production!

q = None
l = None

# Load schemas from files
with open("flask_api/schema/status_schema.json", 'r') as file:
    status_schema = json.load(file)
with open("flask_api/schema/log_message_schema.json", 'r') as file:
    log_message_schema = json.load(file)
with open("flask_api/schema/trough_status_schema.json", 'r') as file:
    trough_status_schema = json.load(file)
with open("flask_api/schema/trough_feature_schema.json", 'r') as file:
    trough_feature_schema = json.load(file)

# Define Endpoints
@socketio.on("status")
def status_endpoint(data):
    return validate_request(data, status_schema, "status")

@socketio.on("log")
def log_endpoint(data):
    return validate_request(data, log_message_schema, "log")

@socketio.on("trough_status")
def trough_status_endpoint(data):
    return validate_request(data, trough_status_schema, "trough_status")

@socketio.on("trough_feature")
def trough_feature_endpoint(data):
    return validate_request(data, trough_feature_schema, "trough_feature")

@socketio.on('connect')
def test_connect(message):
    print("Client connected, message:", message)
    emit("Successfully received")

@socketio.on('disconnect')
def test_disconnect(reason):
    print('Client disconnected, reason:', reason)

def validate_request(data, schema, schema_name):
    global q, l
    try:
        validate(instance=data, schema=schema)
        l.call_soon_threadsafe(q.put_nowait, (
            schema_name,
            data
        ))
        return {"message": "Valid request"}, 200
    except ValidationError as e:
        return {"error": "Invalid request", "details": e.message}, 400
    except Exception as e:
        return {"error": "Something went wrong", "details": str(e)}, 500

# Called externally to start Flask
def run(message_queue, loop):
    global q, l
    q = message_queue
    l = loop
    print("Starting Flask thread\n")
    socketio.run(app, host='0.0.0.0', port=3000, debug=False, use_reloader=False)

if __name__ == '__main__':
    run(None)