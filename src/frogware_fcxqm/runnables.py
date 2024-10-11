import threading
import PyQt5.QtCore as qtc

from .hardware_comms.device_interfaces import Spectrometer, LinearMotor

# Signal class to be used for Runnable


class Signal(qtc.QObject):
    started = qtc.pyqtSignal(object)
    progress = qtc.pyqtSignal(object)
    finished = qtc.pyqtSignal(object)


class UpdateMotorPositionRunnable(qtc.QRunnable):
    def __init__(self, motor: LinearMotor, event_to_clear: threading.Event):
        super().__init__()

        self.motor = motor
        self.signal = Signal()
        self.started = self.signal.started
        self.progress = self.signal.progress
        self.finished = self.signal.finished
        self._stop_initiated = False

        self.event_to_clear = event_to_clear

    """
    I ran into an error where I believe the program was writing two
    messages to the port at the same time (get position, and stop). So,
    it's important to enforce sequential writing to the port. I'm doing that
    by putting the stop command in the run loop.
    """

    def stop(self):
        self._stop_initiated

    def run(self):

        # TODO may be broken. May need to read location from hardware
        while self.motor.is_in_motion():
            pos = self.motor.pos_um()
            self.progress.emit(pos)
            # time.sleep(.001)

        # stop flag has been set to True, and the loop has terminated
        # clear the event
        self.event_to_clear.clear()

        pos = self.motor.pos_um()
        self.progress.emit(pos)
        self.finished.emit(None)


class UpdateSpectrumRunnable(qtc.QRunnable):
    """Runnable class for the ContinuousUpdate class"""

    def __init__(self, spectrometer: Spectrometer, event_to_clear, event_to_set):
        super().__init__()

        # this class takes as input the spectrometer which it will
        # continuously pull the the spectrum from
        self.spectrometer = spectrometer
        # also initialize a signal so you can transmit the spectrum to the
        # main Continuous Update class
        self.signal = Signal()
        self.started = self.signal.started
        self.progress = self.signal.progress
        self.finished = self.signal.finished

        # initialize stop signal to false
        self._stop = False

        event_to_clear: threading.Event
        event_to_set: threading.Event
        self.event_to_clear = event_to_clear
        self.event_to_set = event_to_set

    # set stop signal to true
    def stop(self):
        self._stop = True

    def run(self):
        # while stop is false, continuously get the spectrum
        while not self._stop:
            # get the spectrum
            # wavelengths, intensities = self.spectrometer.spectrum()
            spectrum = self.spectrometer.spectrum()
            # emit the spectrum as a signal
            # self.progress.emit([wavelengths, intensities])
            self.progress.emit(spectrum)

        # stop flag has been set to True, and the loop has terminated
        # clear the event
        self.event_to_clear.clear()
        self.event_to_set.set()
