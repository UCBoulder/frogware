import PyQt5.QtWidgets as qt
import PyQt5.QtCore as qtc
import PlotAndTableFunctions
from Window import Ui_MainWindow
import PlotAndTableFunctions as plotf
import numpy as np
import gc
import utilities as util
import time
from Error import Ui_Form
import PyQt5.QtGui as qtg

# will be used later on for any continuous update of the display that lasts more
# than a few seconds
pool = qtc.QThreadPool.globalInstance()

# the speed of light
c_mks = 299792458


# Signal class to be used for Runnable
class Signal(qtc.QObject):
    started = qtc.pyqtSignal(object)
    progress = qtc.pyqtSignal(object)
    finished = qtc.pyqtSignal(object)


class ErrorWindow(qt.QWidget, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.show()

    def set_text(self, text):
        self.textBrowser.setText(text)


def raise_error(text):
    error_window = ErrorWindow()
    error_window.set_text(text)


class MainWindow(qt.QMainWindow, Ui_MainWindow):
    """
    This is the main GUI window. For better readability and ease of editing later on, I would like to
    move as many widgets as possible into their own separate classes.
    """

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.show()

        # I will eventually delete these, but I have them here for now for reference
        self.plot_cont_upd = plotf.PlotWindow(self.le_cont_upd_xmin, self.le_cont_upd_xmax, self.le_cont_upd_ymin,
                                              self.le_cont_upd_ymax, self.gv_cont_upd_spec)

        self.plot_spectrogram = plotf.PlotWindow(self.le_spectrogram_xmin, self.le_spectrogram_xmax,
                                                 self.le_spectrogram_ymin, self.le_spectrogram_ymax,
                                                 self.gv_Spectrogram)

        self.connect_motor_spectrometer()

    def connect_motor_spectrometer(self):
        # should end up doing something like:
        # serial_number = apt.list_available_devices()[1]
        # motor = apt.Motor(serial_number)
        # self.motor = util.Motor(motor)
        # spectrometer = seabreeze.spectrometers.list_devices()[0]
        # self.spectrometer = util.Spectrometer(spectrometer)
        pass


class MotorInterface:
    """I was thinking to keep classes in utilities.py more bare bone, and focus on hardware
    communication there. Here I will add more things I would like the Motor class to have."""

    def __init__(self, motor):
        motor: util.Motor
        self.motor = motor

        self.T0_um = 0  # T0 position of the motor in micron
        self._pos_um = 0  # position of the motor in micron

        # initialize motor position
        self._pos_um = self.motor.position * 1e6  # assuming they give position in mks?

    @property
    def pos_um(self):
        return self._pos_um

    @property
    def pos_m(self):
        return self._pos_um * 1e-6

    @property
    def pos_fs(self):
        # pos_fs is taken from pos_um and T0_um
        return (self.pos_um - self.T0_um) * 1e9 / c_mks

    @pos_m.setter
    def pos_m(self, value_mks):
        # pos_mks is taken from pos_um, so to set pos_mks just set pos_um
        self.pos_um = value_mks * 1e6

    @pos_um.setter
    def pos_um(self, value_um):
        self._pos_um = value_um

        # move the motor to the new position
        self.motor.position = self.pos_m

    @pos_fs.setter
    def pos_fs(self, value_fs):
        # pos_fs is taken from pos_um, so just set pos_um
        # setting pos_um moves the motor
        self.pos_um = value_fs * 1e-9 * c_mks + self.T0_um

    def move_by_fs(self, value_fs):
        # obtain the distance to move in micron and meters
        value_um = value_fs * 1e-9 * c_mks
        value_m = value_um * 1e-6

        # move the motor to the new position and update the position in micron
        self.motor.move_by(value_m)
        # it is important that you update _pos_um, or else setting pos_um will continue to move the motor
        # in absolute mode to that position.
        self._pos_um += value_um

    def move_by_um(self, value_um):
        value_m = value_um * 1e-6

        # move the motor to the new position and update the position in micron
        # it is important that you update _pos_um, or else setting pos_um will continue to move the motor
        # in absolute mode to that position.
        self.motor.move_by(value_m)
        self._pos_um += value_um


class ContinuousUpdate:
    """
    This class interfaces the Spectrum Continuous Update tab with the main window
    """

    def __init__(self, main_window, motor, spectrometer):
        main_window: MainWindow
        motor: MotorInterface
        spectrometer: util.Spectrometer
        self.main_window = main_window
        self.spectrometer = spectrometer
        self.motor = motor
        self.runnable = UpdateSpectrumRunnable(self.spectrometer)

        # get convenient access to relevant main window attributes
        self.btn_start = self.main_window.btn_start_cnt_update
        self.btn_step_left = self.main_window.btn_step_left
        self.btn_step_right = self.main_window.btn_step_right
        self.le_step_size_um = self.main_window.le_step_size_um
        self.le_step_size_fs = self.main_window.le_step_size_fs
        self.btn_home_stage = self.main_window.btn_home_stage
        self.btn_move_to_pos = self.main_window.btn_move_to_pos
        self.le_pos_um = self.main_window.le_pos_um
        self.le_pos_fs = self.main_window.le_pos_fs
        self.lcd_current_pos_um = self.main_window.lcd_cnt_update_current_pos_um
        self.lcd_current_pos_fs = self.main_window.lcd_cnt_update_current_pos_fs
        self.btn_setT0 = self.main_window.btn_set_T0
        self.plot_window = plotf.PlotWindow(self.main_window.le_cont_upd_xmin, self.main_window.le_cont_upd_xmax,
                                            self.main_window.le_cont_upd_ymin, self.main_window.le_cont_upd_ymax,
                                            self.main_window.gv_cont_upd_spec)
        self.stop = self.main_window.actionStop

        # create a curve and add it to the plotwidget
        self.curve = plotf.create_curve()
        self.plot_window.plotwidget.addItem(self.curve)

        # initialize the step size, 0 is arbitrary
        self._step_size_fs = 0

        # the inputs have to be floats
        self.le_pos_fs.setValidator(qtg.QDoubleValidator())
        self.le_pos_um.setValidator(qtg.QDoubleValidator())
        self.le_step_size_fs.setValidator(qtg.QDoubleValidator())
        self.le_step_size_um.setValidator(qtg.QDoubleValidator())

        self.connect()

    @property
    def step_size_um(self):
        # set the step size in micron based off the step size in fs
        return self._step_size_fs * 1e-9 * c_mks

    @property
    def step_size_fs(self):
        return self._step_size_fs

    @step_size_um.setter
    def step_size_um(self, value_um):
        # step_size_um is based off step_size_fs so just update step_size_fs
        self._step_size_fs = value_um * 1e9 / c_mks

        # update the line edits
        self.update_le_um()
        self.update_le_fs()

    @step_size_fs.setter
    def step_size_fs(self, value_fs):
        self._step_size_fs = value_fs

        # update the line edits
        self.update_le_um()
        self.update_le_fs()

    def update_stepsize_from_le_um(self):
        step_size_um = float(self.le_step_size_um.text())
        self.step_size_um = step_size_um

    def update_stepsize_from_le_fs(self):
        step_size_fs = float(self.le_step_size_fs.text())
        self.step_size_fs = step_size_fs

    def update_le_um(self):
        self.le_step_size_um.setText('%.3f' % self.step_size_um)

    def update_le_fs(self):
        self.le_step_size_fs.setText('%.3f' % self.step_size_fs)

    def connect(self):
        # if the stop action button is pressed, stop the continuous update
        self.stop.triggered.connect(self.stop_continuous_update)
        # if the start continuous update button is pressed start the continuous update
        self.btn_start.clicked.connect(self.start_continuous_update)
        # for each retrieval of the spectrum update the plot in the gui
        self.runnable.progress.connect(self.plot_update)
        # update step size (for both um and fs)
        self.le_step_size_um.editingFinished.connect(self.update_stepsize_from_le_um)
        self.le_step_size_fs.editingFinished.connect(self.update_stepsize_from_le_fs)

    def start_continuous_update(self):
        # start the continuous update
        pool.start(self.runnable)

    def stop_continuous_update(self):
        # stop the continuous update
        self.runnable.stop()

    def plot_update(self, X):
        # the signal should emit wavelengths and intensities
        wavelengths, intensities = X
        # set the data to the new spectrum
        self.curve.setData(x=wavelengths, y=intensities)

    def step_right(self):
        pass

    def step_left(self):
        pass

    def move_to_pos(self):
        pass

    def set_T0(self):
        pass

    def home_stage(self):
        pass


class UpdateSpectrumRunnable(qtc.QRunnable):
    """Runnable class for the ContinuousUpdate class"""

    def __init__(self, spectrometer):
        super().__init__()

        # this class takes as input the spectrometer which it will continuously pull the
        # the spectrum from
        spectrometer: util.Spectrometer
        self.spectrometer = spectrometer
        # also initialize a signal so you can transmit the spectrum to the main Continuous Update class
        self.signal = Signal()
        self.started = self.signal.started
        self.progress = self.signal.progress
        self.finished = self.signal.finished

        # initialize stop signal to false
        self._stop = False

    # set stop signal to true
    def stop(self):
        self._stop = True

    def run(self):
        # while the stop attribute is false, continuously get the spectrum
        while True:
            if not self._stop:
                # get the spectrum
                wavelengths, intensities = self.spectrometer.get_spectrum()
                # emit the spectrum as a signal
                self.progress.emit([wavelengths, intensities])
                # I don't know how fast it does this, so I'm telling it to sleep for .1 seconds. If
                # it turns out that it already takes ~.1s to get the spectrum then you can delete this
                time.sleep(.1)
            else:
                return


if __name__ == '__main__':
    app = qt.QApplication([])
    gui = MainWindow()
    app.exec()
