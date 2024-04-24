import time
import threading
import cv2
from djitellopy import Tello
from devices.generic_presence_sensor import GenericPresenceSensor

sensor = GenericPresenceSensor(port="COM5")
sensor.connect()

drone = Tello()

def run_detect_loop():
    print("Starting to detect")
    while True:
        state = sensor.get_state()
        if state.presence:
            print("PRESENCE DETECTED: Taking off")
            drone.takeoff()
            drone.land()
        print(f"Presence: {state.presence}")
        time.sleep(0.1)

if __name__ == "__main__":
    drone.connect()
    drone.streamon()

    time.sleep(1)

    run_detect_loop()