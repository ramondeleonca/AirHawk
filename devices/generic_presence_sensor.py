import serial
from dataclasses import dataclass

class GenericPresenceSensor:
    @dataclass
    class GenericPresenceSensorState:
        """Presence detected"""
        presence: bool

    port: str
    ser: serial.Serial
    baud: int

    def __init__(self, port: str, baud: int = 115200) -> None:
        self.port = port
        self.baud = baud
        self.ser = serial.Serial(port, baud)

    def connect(self) -> None:
        try:
            self.ser.open()
        except:
            pass
    
    def disconnect(self) -> None:
        self.ser.close()

    def get_raw(self):
        return self.ser.readline().decode('utf-8', "replace").strip()

    def get_state(self):
        state = self.get_raw().lower()
        return GenericPresenceSensor.GenericPresenceSensorState(presence="presence" in state)
