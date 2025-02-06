import socketio
import time
import json

def main():
    with socketio.SimpleClient() as sio:
        sio.connect('http://localhost:5000')
        message = json.dumps({"Testing, testing, testing ..."})
        sio.emit(message)
        time.sleep(10)


if __name__ == '__main__':
    main()