from abc import ABC, abstractmethod
from .utilities import T_fs_to_dist_um, dist_um_to_T_fs
import numpy as np
'''
Abstract class for linear motors
'''


class LinearMotor(ABC):
    '''
    Tuple of the software limits for the stage
    (lower, upper) in microns
    '''
    @property
    def travel_limits_um(self) -> tuple[float]:
        try:
            return self._travel_limits
        except AttributeError:
            raise StageLimitsNotSetException(
                "Motor software limits not initialized")

    @travel_limits_um.setter
    def travel_limits_um(self, limits: tuple[float]) -> None:
        self._travel_limits = limits[:2]

    '''
    Location of the stage corresponding to time zero 
    (i.e. the center of the FROG trace)
    '''
    @property
    def T0_um(self) -> float:
        try:
            return self._T0_um
        except AttributeError:
            try:
                self._read_T0_from_file()
            except FileNotFoundError:
                self._T0_um = self.pos_um()
                self._write_T0_to_file()
            return self._T0_um

    @T0_um.setter
    def T0_um(self, dist_um: float):
        self._T0_um = dist_um

    '''
    Get stage position in microns
    '''
    @abstractmethod
    def pos_um(self) -> float:
        pass

    '''
    Absolute location of the stage (in femtoseconds,
    with respect to time zero)
    '''

    def pos_fs(self) -> float:
        return dist_um_to_T_fs(self.pos_um - self.T0_um)

    '''
    Move the relative position of the stage (femtosecond units)
    Should raise a StageOutOfBoundsException if it
    would exceed the software limits.
    '''

    def move_by_fs(self, value_fs: float) -> None:
        self.move_by_um(T_fs_to_dist_um(value_fs))

    '''
    Move the relative position of the stage (micron units)
    Should raise a StageOutOfBoundsException if it
    would exceed the software limits.
    '''
    @abstractmethod
    def move_by_um(self, value_um: float) -> None:
        pass

    '''
    Move to an absolute location (micron units).
    Should raise a StageOutOfBoundsException if it
    would exceed the software limits.
    '''
    @abstractmethod
    def move_to_um(self, value_um: float) -> None:
        pass

    '''
    Home the stage. blocking indicates whether the program waits until the operation
    is complete
    '''
    @abstractmethod
    def home(self, blocking: bool) -> None:
        pass

    '''
    Checks if the stage is in motion
    '''
    @abstractmethod
    def is_in_motion(self) -> bool:
        pass

    '''
    Stops the stage, interrupting any current operations.
    '''
    @abstractmethod
    def stop(self, blocking: bool) -> None:
        pass

    '''
    Saves T0 to T0_um.txt
    '''

    def _read_T0_from_file(self) -> None:
        with open("T0_um.txt", "r") as file:
            self._T0_um = float(file.readline())

    '''
    Reads T0 from T0_um.txt
    '''

    def _write_T0_to_file(self) -> None:
        with open("T0_um.txt", "w") as file:
            file.write(f'{self._T0_um}')


'''
Abstract class for spectrometers
'''


class Spectrometer(ABC):

    '''Returns the intensities (in arbitrary units)'''
    @abstractmethod
    def intensities(self) -> np.ndarray[np.float_]:
        pass

    '''Returns the wavelength bins (in nanometeres) '''
    @abstractmethod
    def wavelengths(self) -> np.ndarray[np.float_]:
        pass

    '''Returns a 2-D list of the wavelengths (0) and intensities (1)'''
    @abstractmethod
    def spectrum(self) -> np.ndarray[np.float_]:
        pass

    '''Reads the integration time in microseconds'''
    @property
    @abstractmethod
    def integration_time_micros(self) -> int:
        pass

    '''Sets the integration time in microseconds'''
    @integration_time_micros.setter
    @abstractmethod
    def integration_time_micros(self, value) -> None:
        pass

    '''
    Reads the number of scans averaged together in each
    spectrum
    '''
    @property
    @abstractmethod
    def scans_to_avg(self) -> int:
        pass

    '''Sets the number of scans averaged together in each spectrum'''
    @scans_to_avg.setter
    @abstractmethod
    def scans_to_avg(self, N) -> None:
        pass

    @property
    @abstractmethod
    def integration_time_micros_limit(self) -> tuple[int, int]:
        pass


class StageOutOfBoundsException(Exception):
    def __init__(self, message):
        self.message = message


class StageLimitsNotSetException(Exception):
    def __init__(self, message):
        self.message = message


class SpectrometerIntegrationException(Exception):
    def __init__(self, message):
        self.message = message


class SpectrometerAverageException(Exception):
    def __init__(self, message):
        self.message = message
