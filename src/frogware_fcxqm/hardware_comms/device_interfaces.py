from abc import ABC, abstractmethod
import numpy as np
from platformdirs import user_data_path
from pathlib import Path

from .utilities import T_fs_to_dist_um, dist_um_to_T_fs

'''
Abstract class for linear motors. Implement this with a subclass for
new motor devices.
'''


class LinearMotor(ABC):
    '''
    Software limits for the stage

    returns: (lower bound, upper bound), in microns
    raises: StageLimitsNotSetException if limits are not
    set
    '''
    @property
    def travel_limits_um(self) -> tuple[float]:
        try:
            return self._travel_limits
        except AttributeError:
            raise StageLimitsNotSetException(
                "Motor software limits not initialized")

    '''
    Sets software limits of the stage. Should be initialized in 
    .connect_devices.connect_devices() or the constructor for the
    subclass.
    
    limits: listlike containing (lower bound, upper bound), in microns
    '''

    @travel_limits_um.setter
    def travel_limits_um(self, limits: tuple[float]) -> None:
        self._travel_limits = limits[:2]

    '''
    Location of the stage corresponding to time zero 
    (i.e. the center of the FROG trace). Calls self._read_T0_from_file()
    and self._write_T0_to_file() to save T0 to persistent storage between
    program executions.

    returns: float of stage displacement at time zero, in microns
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

    '''
    Sets the stage location corresponding to time zero.
    
    dist_um: stage location in microns
    '''
    @T0_um.setter
    def T0_um(self, dist_um: float):
        self._T0_um = dist_um
        self._write_T0_to_file()

    '''
    Get stage position in microns

    returns: location of the stage, in microns
    '''
    @abstractmethod
    def pos_um(self) -> float:
        pass

    '''
    Get stage location in femtoseconds, with respect to time zero.

    returns: float of the stage location, in femtoseconds
    '''

    def pos_fs(self) -> float:
        return dist_um_to_T_fs(self.pos_um - self.T0_um)

    '''
    Move the relative position of the stage (micron units).

    value_um: distance of relative move (positive or negative), in microns
    raises: StageOutOfBoundException if the move would exceed
    the software limits of the stage.
    '''

    @abstractmethod
    def move_by_um(self, value_um: float) -> None:
        pass

    '''
    Move the relative position of the stage (femtosecond units)
    
    value_fs: distance of the relative move (positive or negative), in
    femtoseconds
    raises: StageOutOfBoundException if the move would exceed
    the software limits of the stage.
    '''

    def move_by_fs(self, value_fs: float) -> None:
        self.move_by_um(T_fs_to_dist_um(value_fs))

    '''
    Move to an absolute location (micron units).

    value_um: desired stage location, in microns
    raises: StageOutOfBoundException if the move would exceed
    the software limits of the stage.
    '''
    @abstractmethod
    def move_to_um(self, value_um: float) -> None:
        pass

    '''
    Move to an absolute location (femtosecond units).

    value_fs: desired stage location, in femtoseconds
    raises: StageOutOfBoundException if the move would exceed
    the software limits of the stage.
    '''

    def move_to_um(self, value_fs: float) -> None:
        self.move_to_um(T_fs_to_dist_um(value_fs))

    '''
    Home the stage. 

    blocking: True if program should pause until the stage is homed.
    False otherwise.
    '''
    @abstractmethod
    def home(self, blocking=False) -> None:
        pass

    '''
    Checks if the stage is in motion.
    
    returns: True if stage is in motion. False otherwise.
    '''
    @abstractmethod
    def is_in_motion(self) -> bool:
        pass

    '''
    Stops the stage, interrupting any current operations.

    blocking: True if program should pause until the stage is homed.
    False otherwise.
    '''
    @abstractmethod
    def stop(self, blocking=True) -> None:
        pass

    '''
    Closes the backend to avoid hanging processes.
    '''
    @abstractmethod
    def close(self) -> None:
        pass

    '''
    Location on the filesystem for persistent storage of configuration information
    
    returns: pathlib Path to the directory for persistent storage
    '''
    @property
    def datapath(self) -> Path:
        return user_data_path(appname='frogware', appauthor='FCxQM')

    '''
    Saves T0 to T0_um.txt in the directory defined by self.datapath
    '''

    def _read_T0_from_file(self) -> None:
        with open(self.datapath / "T0.txt", "r") as file:
            self._T0_um = float(file.readline())

    '''
    Reads T0 from T0_um.txt in the directory defined by self.datapath
    '''

    def _write_T0_to_file(self) -> None:
        with open(self.datapath / "T0_um.txt", "w") as file:
            file.write(f'{self._T0_um}')


'''
Abstract class for spectrometers
'''


class Spectrometer(ABC):

    '''
    The intensities read by each pixel in the spectrometer (in arbitrary units).

    returns: NDArray of floats corresponding to the intensity in arbitrary units
    '''
    @abstractmethod
    def intensities(self) -> np.ndarray[np.float64]:
        pass

    '''
    Returns the wavelength bins (in nanometers).
    
    returns: NDArray of floats enumarating the wavelength bins in nanometers'''
    @abstractmethod
    def wavelengths(self) -> np.ndarray[np.float64]:
        pass

    '''
    Returns a 2-D list of the wavelengths (0) and intensities (1)

    returns: 2DArray where,
            [0] = wavelengths
            [1] = intensities
    '''
    @abstractmethod
    def spectrum(self) -> np.ndarray[np.float64]:
        pass

    '''
    Reads the integration time in microseconds.
    
    return: hardware integration time, in microseconds
    '''
    @property
    @abstractmethod
    def integration_time_micros(self) -> int:
        pass

    '''
    Sets the integration time in microseconds
    
    value: integration time, in microseconds
    '''
    @integration_time_micros.setter
    @abstractmethod
    def integration_time_micros(self, value) -> None:
        pass

    '''
    Reads the number of scans averaged together in each
    spectrum.
    
    returns: number of averages per spectrum
    '''
    @property
    @abstractmethod
    def scans_to_avg(self) -> int:
        pass

    '''
    Sets the number of scans averaged together in each spectrum.

    N: number of averages per spectrum
    '''
    @scans_to_avg.setter
    @abstractmethod
    def scans_to_avg(self, N) -> None:
        pass

    '''
    Returns the integration time in microseconds.

    return: listlike of (lower bound, upper bound) in microseconds
    '''
    @property
    @abstractmethod
    def integration_time_micros_limit(self) -> tuple[int, int]:
        pass

    '''
    Closes the backend to avoid hanging processes.
    '''
    @abstractmethod
    def close(self) -> None:
        pass


class StageOutOfBoundsException(Exception):
    def __init__(self, message):
        self.message = message


class StageLimitsNotSetException(Exception):
    def __init__(self, message):
        self.message = message


class StageNotCalibratedException(Exception):
    def __init__(self, message):
        self.message = message


class SpectrometerIntegrationException(Exception):
    def __init__(self, message):
        self.message = message


class SpectrometerAverageException(Exception):
    def __init__(self, message):
        self.message = message


class DeviceCommsException(Exception):
    def __init__(self, message):
        self.message = message
