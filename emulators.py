import numpy as np
import matplotlib.pyplot as plt


class Motor:
    def __init__(self):
        pass

        self.position = 0
        self._is_in_motion = False

    def move_by(self):
        pass

    def move_home(self):
        pass

    def stop_motor(self):
        pass

    @property
    def is_in_motion(self):
        return self._is_in_motion

    def stop_profiled(self):
        pass

    def get_stage_axis_info(self):
        pass


class Spectrometer:
    def __init__(self):
        self.int_time_micros = 1000
        self.integration_time_micros_limits = [1, 10e6]

    def spectrum(self):
        wavelengths = np.linspace(350, 1150, 5000)
        lambda0 = 25 + 5 * np.random.random()
        intensities = 1 / np.cosh((wavelengths - 750) / lambda0)
        return wavelengths, intensities

    def integration_time_micros(self, time_micros):
        self.int_time_micros = time_micros
