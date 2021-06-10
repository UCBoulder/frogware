"""This file should handle all the direct hardware interfacing"""


# import thorlabs_apt as apt
# import seabreeze.spectrometers as spec


class Spectrometer:
    """
    If you don't end up using an Ocean Optics spectrometer, you can
    incorporate your spectrometer into the GUI by writing a class with the
    same attributes and methods as this one.
    """

    def __init__(self, spectrometer):
        # spectrometer: spec.Spectrometer
        self.spectrometer = spectrometer

        self._integration_time_micros = 1000  # 1ms

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
        The Spectrometer class already has a built in function to check that
        you don't set the integration time beyond these limits
        """
        return self.spectrometer.integration_time_micros_limits


class Motor:
    """
    This is a motor class that uses the thorlabs_apt package.
    """

    def __init__(self, motor):
        # motor: apt.Motor
        self.motor = motor

        self._min_pos, self._max_pos, self._units, self._pitch = \
            self.motor.get_stage_axis_info()

    @property
    def position_mm(self):
        # returns the motor position
        return self.motor.position

    @property
    def max_pos_mm(self):
        return self._max_pos

    @property
    def min_pos_mm(self):
        return self._min_pos

    @property
    def units(self):
        return self._units

    @position_mm.setter
    def position_mm(self, value):
        # setting the motor position tells the motor to move in absolute mode
        # and is non-blocking
        self.motor.position = value

    @property
    def is_in_motion(self):
        # is the motor currently in motion?
        return self.motor.is_in_motion

    def move_by(self, value, blocking=False):
        # move relative
        self.motor.move_by(value, blocking)

    def home_motor(self, blocking=False):
        # home the motor
        self.motor.move_home(blocking)

    def stop_motor(self):
        self.motor.stop_profiled()
