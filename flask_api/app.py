from flask import Flask, request, jsonify, render_template
from flask_socketio import SocketIO, emit


app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins='*') #Change for production!
#foxglove = "ws://localhost:8765" #Address to connect to Foxglove

@socketio.on('data_receive')
def handle_json(json):
    print('Received json: ' + str(json))

@socketio.on('connect')
def test_connect(message):
    print("Success:", message)
    emit("Successfully received")

@socketio.on('disconnect')
def test_disconnect(reason):
    print('Client disconnected, reason:', reason)


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
    socketio.run(app, port=5000, debug=True)