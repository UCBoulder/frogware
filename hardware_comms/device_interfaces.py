from Gui_Controller import ErrorWindow, edge_limit_buffer_mm, raise_error
from abc import ABC, abstractmethod
from scipy.constants import c as C_MKS

class Motor(ABC):
    def __init__(self):
        self.T0_um = 0  # T0 position of the motor in micron
        # don't let the stage come closer than this to the stage limits.
        self._safety_buffer_mm = edge_limit_buffer_mm  # 1um

        self.error_window = ErrorWindow()

    @property
    @abstractmethod
    def pos_um(self):
        pass
        

    @property
    @abstractmethod
    def pos_fs(self):
        # pos_fs is taken from pos_um and T0_um
        pass
        return dist_um_to_T_fs(self.pos_um - self.T0_um)

    @pos_um.setter
    @abstractmethod
    def pos_um(self, value_um):
        # move the motor to the new position, assuming they give the motor
        # position in mm
        pass
        self.motor.position_mm = value_um * 1e-3

    @pos_fs.setter
    @abstractmethod
    def pos_fs(self, value_fs):
        # pos_fs is taken from pos_um, so just set pos_um
        # setting pos_um moves the motor
        self.pos_um = T_fs_to_dist_um(value_fs) + self.T0_um

    @abstractmethod
    def move_by_fs(self, value_fs):
        # obtain the distance to move in micron and meters
        value_um = T_fs_to_dist_um(value_fs)
        value_mm = value_um * 1e-3

        # move the motor to the new position and update the position in micron
        self.motor.move_by(value_mm)

    @abstractmethod
    def move_by_um(self, value_um):
        value_mm = value_um * 1e-3

        # move the motor to the new position and update the position in micron
        self.motor.move_by(value_mm)

    @abstractmethod
    def value_exceeds_limits(self, value_um):
        predicted_pos_um = value_um + self.pos_um
        max_limit_um = self.motor.max_pos_mm * 1e3
        min_limit_um = self.motor.min_pos_mm * 1e3
        buffer_um = self._safety_buffer_mm * 1e3

        if (predicted_pos_um < min_limit_um + buffer_um) or (
            predicted_pos_um > max_limit_um - buffer_um
        ):
            raise_error(self.error_window, "too close to stage limits (within 1um)")
            return True
        else:
            return False
    @staticmethod
    def dist_um_to_T_fs(value_um):
        """
        :param value_um: delta x in micron
        :return value_fs: delta t in femtosecond
        """
        return (2 * value_um / C_MKS) * 1e9

    @staticmethod
    def T_fs_to_dist_um(value_fs):
        """
        :param value_fs: delta t in femtosecond
        :return value_um: delta x in micron
        """
        return (C_MKS * value_fs / 2) * 1e-9


class Spectrometer(ABC):
    """
    This class expects a spectrometer instance. You can incorporate a
    spectrometer and pass it to here by creating a spectrometer class with
    the following attributes and methods:

    methods:

        1. spectrum(): returns wavelengths, intensities

        2. wavelengths(): returns wavelengths

        3. integration_time_micros(integration_time_micros): sets the
        integration time in microseconds


    attributes:

        1. integration_time_micros_limits: [min_int_time_us, max_int_time_us]

    """

    def __init__(self, spectrometer):
        self.spectrometer = spectrometer

        # initialize the integration time and number of scans to average to some value, and then update the actual
        # spectrometer integration time in MainWindow (so the value here doesn't matter)
        self._integration_time_micros = 30000
        self._scans_to_avg = 1

    @abstractmethod
    def get_spectrum(self):
        """
        :return: wavelengths, intensities
        """
        pass
    @property
    @abstractmethod
    def wavelengths(self):
        return self.spectrometer.wavelengths()

    @property
    @abstractmethod
    def integration_time_micros(self):
        return self._integration_time_micros

    @integration_time_micros.setter
    @abstractmethod
    def integration_time_micros(self, value):
        self._integration_time_micros = value
        self.spectrometer.integration_time_micros(self._integration_time_micros)

    @property
    @abstractmethod
    def scans_to_avg(self):
        return self._scans_to_avg

    @scans_to_avg.setter
    @abstractmethod
    def scans_to_avg(self, N):
        self._scans_to_avg = N
        self.spectrometer.set_scans_to_average(N)

    @property
    @abstractmethod
    def integration_time_micros_limit(self):
        """
        The Spectrometer class already has a built in function to check that
        you don't set the integration time beyond these limits
        """
        return self.spectrometer.integration_time_micros_limitsclass 