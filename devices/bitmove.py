import serial
import json
from dataclasses import dataclass

class BitMove:
    @dataclass
    class BitMoveState:
        """RAM memory usage"""
        memoryUsage: float

        """ROM memory usage"""
        diskUsage: float

        """Sensor update delta time"""
        deltaTime: int

        """Device uptime"""
        uptime: int

        # Device functionality

        """Presence detected"""
        present: bool

    port: str
    ser: serial.Serial
    baud: int

    def __init__(self, port: str, baud: int = 115200) -> None:
        self.port = port
        self.baud = baud
        self.ser = serial.Serial(port, baud)

    def connect(self) -> None:
        self.ser.open()
    
    def disconnect(self) -> None:
        self.ser.close()

    def get_state(self):
        self.ser.write(b'get_state\n')
        state = self.ser.readline().decode('utf-8', "replace")
        state = json.loads(state)
        return BitMove.BitMoveState(**state)
