from flask import Flask, request, jsonify, render_template
from flask_socketio import SocketIO, emit
import json
from jsonschema import validate, ValidationError

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins='*') #Change for production!

# Load schemas from files
with open("flask_api/schema/status_schema.json", 'r') as file:
    status_schema = json.load(file)
with open("flask_api/schema/log_message_schema.json", 'r') as file:
    log_message_schema = json.load(file)

# Define Endpoints
@socketio.on("status")
def status_endpoint(data):
    return validate_request(data, status_schema)

@socketio.on("log")
def log_endpoint(data):
    return validate_request(data, log_message_schema)

@socketio.on('connect')
def test_connect(message):
    print("Client connected, message:", message)
    emit("Successfully received")

@socketio.on('disconnect')
def test_disconnect(reason):
    print('Client disconnected, reason:', reason)

def validate_request(data, schema):
    try:
        validate(instance=data, schema=schema)
        return {"message": "Valid request"}, 200
    except ValidationError as e:
        return {"error": "Invalid request", "details": e.message}, 400
    except Exception as e:
        return {"error": "Something went wrong", "details": str(e)}, 500

if __name__ == '__main__':
    socketio.run(app, port=3000, debug=True)