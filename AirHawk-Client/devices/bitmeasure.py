import serial
import json
from dataclasses import dataclass

class BitMeasure:
    @dataclass
    class BitMeasureState:
        """RAM memory usage"""
        memoryUsage: float

        """ROM memory usage"""
        diskUsage: float

        """Sensor update delta time"""
        deltaTime: int

        """Device uptime"""
        uptime: int

        # Device functionality
        """Distance measured by the sensor [4-400]cm"""
        distance: float

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
        return self.ser.readline().decode('utf-8', "replace")

    def get_state(self):
        self.ser.write(b'get_state\n')
        state = self.get_raw()
        state = json.loads(state)
        return BitMeasure.BitMeasureState(**state)
