import PyQt5.QtWidgets as qt
import PyQt5.QtCore as qtc

import PlotAndTableFunctions
from Window import Ui_MainWindow
import PlotAndTableFunctions as plotf
import numpy as np
import gc
import utilities as util

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


class MainWindow(qt.QMainWindow, Ui_MainWindow):
    """
    This is the main GUI window. For better readability and ease of editing later on, I would like to
    move as many widgets as possible into their own separate classes.
    """

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.show()

        # I will eventually delete these
        self.plot_cont_upd = plotf.PlotWindow(self.le_cont_upd_xmin, self.le_cont_upd_xmax, self.le_cont_upd_ymin,
                                              self.le_cont_upd_ymax, self.gv_cont_upd_spec)

        self.plot_spectrogram = plotf.PlotWindow(self.le_spectrogram_xmin, self.le_spectrogram_xmax,
                                                 self.le_spectrogram_ymin, self.le_spectrogram_ymax,
                                                 self.gv_Spectrogram)

        self.connect_motor_spectrometer()

    def connect_motor_spectrometer(self):
        # should end up doing something like
        # serial_number = apt.list_available_devices()[1]
        # motor = apt.Motor(serial_number)
        # self.motor = util.Motor(motor)
        # spectrometer = seabreeze.spectrometers.Spectrometer.from_first_available()
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
        self._pos_fs = 0  # position of the motor in fs (requires knowledge of T0_um)

        # initialize motor position
        self._pos_um = self.motor.position * 1e6  # assuming they give position in mks?

    @property
    def pos_um(self):
        return self._pos_um

    @property
    def pos_mks(self):
        return self._pos_um * 1e-6

    @property
    def pos_fs(self):
        return self._pos_fs

    @pos_mks.setter
    def pos_mks(self, value_mks):
        # pos_mks is taken from pos_um, so to set pos_mks just set pos_um
        self.pos_um = value_mks * 1e6

    @pos_um.setter
    def pos_um(self, value_um):
        self._pos_um = value_um
        # set the position in fs based on T0_um
        self._pos_fs = (value_um - self.T0_um) * 1e9 / c_mks

        # move the motor to the new position
        self.motor.position = self.pos_mks

    @pos_fs.setter
    def pos_fs(self, value_fs):
        self._pos_fs = value_fs
        # set the position in micron based on T0_um
        self._pos_um = value_fs * 1e-9 * c_mks + self.T0_um

        # move th motor to the new position
        self.motor.position = self.pos_mks

    def move_by_fs(self, value_fs):
        # obtain the distance to move in micron and meters
        value_um = value_fs * 1e-9 * c_mks
        value_mks = value_um * 1e-6

        # move the motor to the new position and update the position in micron
        self.motor.move_by(value_mks)
        # it is important that you update _pos_um, or else setting pos_um will continue to move the motor
        # in absolute mode to that position.
        self._pos_um += value_um

    def move_by_um(self, value_um):
        value_mks = value_um * 1e-6

        # move the motor to the new position and update the position in micron
        # it is important that you update _pos_um, or else setting pos_um will continue to move the motor
        # in absolute mode to that position.
        self.motor.move_by(value_mks)
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

        self.connect()

    def connect(self):
        pass


if __name__ == '__main__':
    app = qt.QApplication([])
    gui = MainWindow()
    app.exec()
