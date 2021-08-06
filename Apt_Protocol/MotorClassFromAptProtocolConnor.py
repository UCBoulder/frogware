import APT as apt
import struct
from APT import _auto_connect
import numpy as np


class KDC101(apt.KDC101_PRM1Z8):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @property
    def is_in_motion(self):
        status = self.status()["flags"]
        to_check = [
            status["moving forward"],
            status["moving reverse"],
            status["jogging forward"],
            status["jogging reverse"],
            status["homing"]
        ]
        return np.any(to_check)

    @property
    def position(self):
        return super().position()

    @position.setter
    def position(self, value_mm):
        # assuming it's in millimeters
        super().position(position=value_mm)

    def move_to(self, value_mm):
        self.position = value_mm

    def move_by(self, value_mm, blocking=False):
        self.move_relative(value_mm)

    def move_home(self, blocking):
        self.home(True)

    @_auto_connect
    def stop_profiled(self):
        write_buffer = struct.pack("<BBBBBB", 0x65, 0x04, 0x01, 0x02,
                                   self.dst,
                                   self.src)
        self.write(write_buffer)
