import serial
import json
from dataclasses import dataclass

class BitMove:
    @dataclass
    class BitMoveState:
        # Raw state
        """Raw state"""
        raw: dict

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
    state: BitMoveState

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
        state = BitMove.BitMoveState(**state, raw=state)
        self.state = state
        return state

    def serialize(self):
        return {
            "sensor": {
                "type": self.__class__.__name__,
                "port": self.port,
                "baud": self.baud
            },
            "state": self.state.raw
        }

    def __str__(self) -> str:
        return f"BitMove(port={self.port}, baud={self.baud})"