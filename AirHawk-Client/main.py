import cv2
import scripts.build
from flask_socketio import SocketIO, emit
from flask import Flask, Response, send_from_directory

# * GLOBAL VARIABLES
DEBUG = True
FRONTEND_DIR = "frontend/dist"

# * BACKEND SERVER
cameras: dict[str, cv2.VideoCapture] = {}

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
    if camera_id not in cameras:
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

# * WEBSOCKET SERVER
socketio = SocketIO(app, cors_allowed_origins="*", async_mode="threading")

# * WEBSOCKET EVENTS
@socketio.on("connect")
def handle_connect():
    print("Client connected")

@socketio.on("disconnect")
def handle_disconnect():
    print("Client disconnected")

@socketio.on("message")
def handle_message(message):
    print(f"Received message: {message}")
    emit("message", message)

# * PROGRAM ENTRY POINT
def main():
    # Build frontend
    if not DEBUG:
        print("Rebuilding frontend...")
        scripts.build.build()
    else:
        print("Running in debug mode")

    # Start backend server
    print("Starting backend server...")
    app.run(port=5000)

if __name__ == "__main__":
    main()