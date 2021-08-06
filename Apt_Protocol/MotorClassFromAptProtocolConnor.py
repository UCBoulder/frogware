import APT as apt
import struct


class KDC101(apt.KDC101_PRM1Z8):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @property
    def is_in_motion(self):
        status = self.status()
        return not status["flags"]["settled"]

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
        self.home()

    def stop_profiled(self):
        write_buffer = struct.pack("<BBBBBB", 0x66, 0x04, 0x0E, 0x02, self.dst,
                                   self.src)
        self.write(write_buffer)


