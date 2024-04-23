import time
from devices.generic_presence_sensor import GenericPresenceSensor

sensor = GenericPresenceSensor(port="COM24")
sensor.connect()

while True:
    state = sensor.get_state()
    print(f"Presence: {state.presence}")
    time.sleep(0.1)