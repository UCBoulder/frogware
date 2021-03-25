import numpy as np
import matplotlib.pyplot as plt
import thorlabs_apt as apt
import seabreeze.spectrometers as spec
import pyqtgraph as pg


class Spectrometer:
    def __init__(self, spectrometer):
        spectrometer: spec.Spectrometer
        self.spectrometer = spectrometer

        self._integration_time_micros = None

    def get_spectrum(self):
        """
        :return: wavelengths, intensities
        """
        return self.spectrometer.spectrum()

    @property
    def integration_time_micros(self):
        return self._integration_time_micros

    @integration_time_micros.setter
    def integration_time_micros(self, value):
        self._integration_time_micros = value
        self.spectrometer.integration_time_micros(self._integration_time_micros)

    @property
    def integration_time_micros_limit(self):
        """
        The Spectrometer class already has a built in function to check that you don't set the
        integration time beyond these limits
        """
        return self.spectrometer.integration_time_micros_limits


class Motor:
    def __init__(self, motor):
        motor: apt.Motor
        self.motor = motor

    @property
    def position(self):
        return self.motor.position

    @position.setter
    def position(self, value):
        self.motor.position = value

    def move_by(self, value, blocking=False):
        self.motor.move_by(value, blocking)

    def home_motor(self, blocking=False):
        self.motor.move_home(blocking)
