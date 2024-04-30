import cv2
import webview
import scripts.build
import json
import websockets
import threading
import time
from devices.bitmove import BitMove
from cache import Cache
from djitellopy import Tello
from flask_socketio import SocketIO, emit
from flask import Flask, Response, send_from_directory

# * GLOBAL VARIABLES
PORT = 80
DEBUG = False
DEV = True
FRONTEND_DIR = "frontend/dist"

# * BACKEND SERVER
cameras: dict[str, cv2.VideoCapture] = {}

# * DRONE CONTROL
tello = Tello(host=Tello.TELLO_IP if not DEBUG else "localhost")

# * CACHE
cache = Cache("cache.json")

# * FRONTEND SERVER
app = Flask(__name__)

# * FRONTEND ROUTES
@app.route('/<path:path>')
def static_file(path):
    return send_from_directory(FRONTEND_DIR, path)

@app.route('/')
def index():
    return send_from_directory(FRONTEND_DIR, 'index.html')

@app.route('/camera/<int:camera_id>')
def camera(camera_id):
    if not camera_id in cameras:
        try:
            cameras[camera_id] = cv2.VideoCapture(camera_id)
        except:
            return "Camera not found", 404
    camera = cameras[camera_id]
    def generate_frames():
        while True:
            success, frame = camera.read()
            if not success:
                break
            else:
                ret, buffer = cv2.imencode('.jpg', frame)
                frame = buffer.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/drone/camera')
def drone_camera():
    def generate_frames():
        while True:
            try:
                frame = tello.get_frame_read().frame
                frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
                ret, buffer = cv2.imencode('.jpg', frame)
                frame = buffer.tobytes()
                yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            except:
                pass
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route("/drone/takeoff")
def drone_takeoff():
    tello.takeoff()
    return "OK"

@app.route("/drone/connect")
def drone_connect():
    tello.connect()
    tello.streamon()
    return "OK"

@app.route("/drone/land")
def drone_land():
    tello.land()
    return "OK"

@app.route("/drone/ccw")
def drone_ccw():
    tello.rotate_counter_clockwise(90)
    return "OK"

@app.route("/drone/cw")
def drone_cw():
    tello.rotate_clockwise(90)
    return "OK"

@app.route("/drone/up")
def drone_up():
    tello.move_up(50)
    return "OK"

@app.route("/drone/down")
def drone_down():
    tello.move_down(50)
    return "OK"

@app.route("/drone/left")
def drone_left():
    tello.move_left(50)
    return "OK"

@app.route("/drone/right")
def drone_right():
    tello.move_right(50)
    return "OK"

@app.route("/drone/fwd")
def drone_fwd():
    tello.move_forward(50)
    return "OK"

@app.route("/cache/get/<key>")
def cache_get(key):
    return cache.get(key)

@app.route("/cache/set/<key>/<value>")
def cache_set(key, value):
    cache.set(key, value)
    return "OK"

# * WEBSOCKET SERVER
socketio = SocketIO(app, cors_allowed_origins="*", async_mode="threading")

# * WEBSOCKET EVENTS
@socketio.on("connect")
def handle_connect():
    print("Client connected")

@socketio.on("disconnect")
def handle_disconnect():
    print("Client disconnected")

# * WEBVIEW WINDOW
window = webview.create_window(
    title="AirHawk Surveillance",
    url="http://localhost:" + str(PORT),
    min_size=(800, 600),
    zoomable=True
)

# * PROGRAM ENTRY
def connect_to_drone():
    print("Connecting to Tello drone")
    try:
        tello.connect()
        tello.streamon()
        print("Connected to Tello drone")
    except:
        print("Failed to connect to Tello drone")

def sensor_loop():
    sensor = BitMove("COM8")
    while True:
        print("loop")
        print(sensor.get_state())
        socketio.emit("sensors", sensor.serialize())
        time.sleep(0.1)

def run_backend():
    # Attempt to connect to drone
    threading.Thread(target=connect_to_drone).start()

    # Start sensor loop
    threading.Thread(target=sensor_loop, daemon=True).start()

    # Start backend servers
    print("Starting backend server...")
    app.run(port=PORT)


def main():
    # Build frontend UI
    if not DEBUG:
        print("Rebuilding frontend...")
        scripts.build.build()
    else:
        print("Running in debug mode")
    
    # Start webview and run backend
    webview.start(func=run_backend, debug=DEV)

if __name__ == "__main__":
    main()