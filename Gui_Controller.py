import threading
import PyQt5.QtWidgets as qt
import PyQt5.QtCore as qtc
from Window import Ui_MainWindow
import PlotAndTableFunctions as plotf
import numpy as np
import gc
import utilities as util
import time
from Error import Ui_Form
import PyQt5.QtGui as qtg
import emulators as em
from scipy.constants import c as c_mks

# will be used later on for any continuous update of the display that lasts more
# than a few seconds
pool = qtc.QThreadPool.globalInstance()


def dist_um_to_T_fs(value_um):
    """
    :param value_um: delta x in micron
    :return value_fs: delta t in femtosecond
    """
    return (2 * value_um / c_mks) * 1e9


def T_fs_to_dist_um(value_fs):
    """
    :param value_fs: delta t in femtosecond
    :return value_um: delta x in micron
    """
    return (c_mks * value_fs / 2) * 1e-9


# Signal class to be used for Runnable
class Signal(qtc.QObject):
    started = qtc.pyqtSignal(object)
    progress = qtc.pyqtSignal(object)
    finished = qtc.pyqtSignal(object)


# Popup error window
class ErrorWindow(qt.QWidget, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

    def set_text(self, text):
        self.textBrowser.setText(text)


def raise_error(error_window, text):
    error_window.set_text(text)
    error_window.show()


class MainWindow(qt.QMainWindow, Ui_MainWindow):
    """
    This is the main GUI window. For better readability and ease of editing
    later on, I would like to move as many widgets as possible into their own
    separate classes.
    """

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.show()

        # I will eventually delete these, but I have them here for now for
        # reference (or else I'll forget and have to remember what to write
        # again)
        # self.plot_cont_upd = plotf.PlotWindow(self.le_cont_upd_xmin,
        #                                       self.le_cont_upd_xmax,
        #                                       self.le_cont_upd_ymin,
        #                                       self.le_cont_upd_ymax,
        #                                       self.gv_cont_upd_spec)
        #
        # self.plot_spectrogram = plotf.PlotWindow(self.le_spectrogram_xmin,
        #                                          self.le_spectrogram_xmax,
        #                                          self.le_spectrogram_ymin,
        #                                          self.le_spectrogram_ymax,
        #                                          self.gv_Spectrogram)

        self.connect_motor_spectrometer()

        self.continuous_update_tab = ContinuousUpdate(self,
                                                      self.motor_interface,
                                                      self.spectrometer)

    def connect_motor_spectrometer(self):
        # should end up doing something like:
        # serial_number = apt.list_available_devices()[1]
        # motor = apt.Motor(serial_number)
        # self.motor = MotorInterface(util.Motor(motor))
        # spectrometer = seabreeze.spectrometers.list_devices()[0]
        # self.spectrometer = util.Spectrometer(spectrometer)

        self.motor_interface = MotorInterface(util.Motor(em.Motor()))
        self.spectrometer = util.Spectrometer(em.Spectrometer())
        # pass


class MotorInterface:
    """I was thinking to keep classes in utilities.py more bare bone,
    and focus on hardware communication there. Here I will add more things I
    would like the Motor class to have. """

    def __init__(self, motor):
        motor: util.Motor
        self.motor = motor

        self.T0_um = 0  # T0 position of the motor in micron

        # don't let the stage come closer than this to the stage limits.
        self._safety_buffer_mm = 1e-3  # 1um

        self.error_window = ErrorWindow()

    @property
    def pos_um(self):
        return self.motor.position_mm * 1e3

    @property
    def pos_fs(self):
        # pos_fs is taken from pos_um and T0_um
        return dist_um_to_T_fs(self.pos_um - self.T0_um)

    @pos_um.setter
    def pos_um(self, value_um):
        # move the motor to the new position, assuming they give the motor
        # position in mm
        self.motor.position_mm = value_um * 1e-3

    @pos_fs.setter
    def pos_fs(self, value_fs):
        # pos_fs is taken from pos_um, so just set pos_um
        # setting pos_um moves the motor
        self.pos_um = T_fs_to_dist_um(value_fs) + self.T0_um

    def move_by_fs(self, value_fs):
        # obtain the distance to move in micron and meters
        value_um = T_fs_to_dist_um(value_fs)
        value_mm = value_um * 1e-3

        # move the motor to the new position and update the position in micron
        self.motor.move_by(value_mm)

    def move_by_um(self, value_um):
        value_mm = value_um * 1e-3

        # move the motor to the new position and update the position in micron
        self.motor.move_by(value_mm)

    def value_exceeds_limits(self, value_um):
        predicted_pos_um = value_um + self.pos_um
        max_limit_um = self.motor.max_pos_mm * 1e3
        min_limit_um = self.motor.min_pos_mm * 1e3
        buffer_um = self._safety_buffer_mm * 1e3

        if (predicted_pos_um < min_limit_um + buffer_um) or (
                predicted_pos_um > max_limit_um - buffer_um):
            print("I raised an error!")
            raise_error(self.error_window,
                        "too close to stage limits (within 1um)")
            return True
        else:
            return False


class ContinuousUpdate:
    """
    This class interfaces the Spectrum Continuous Update tab with the main
    window. It expects an instance of the MainWindow, MotorInterface,
    and util.Spectrometer class in the init function.
    """

    def __init__(self, main_window, motor_interface, spectrometer):
        """
        :param main_window:
        :param motor_interface:
        :param spectrometer:
        """

        main_window: MainWindow
        motor_interface: MotorInterface
        spectrometer: util.Spectrometer
        self.main_window = main_window
        self.spectrometer = spectrometer
        self.motor_interface = motor_interface

        # get convenient access to relevant main window attributes
        self.btn_start = self.main_window.btn_start_cnt_update
        self.btn_step_left = self.main_window.btn_step_left
        self.btn_step_right = self.main_window.btn_step_right
        self.btn_collect_spectrogram = self.main_window.btn_collect_spectrogram
        self.le_step_size_um = self.main_window.le_step_size_um
        self.le_step_size_fs = self.main_window.le_step_size_fs
        self.le_step_size_um_tab2 = self.main_window.le_tab2_step_size_um
        self.le_step_size_fs_tab2 = self.main_window.le_tab2_step_size_fs
        self.le_startpos_um = self.main_window.le_start_um
        self.le_startpos_fs = self.main_window.le_start_fs
        self.le_endpos_um = self.main_window.le_end_um
        self.le_endpos_fs = self.main_window.le_end_fs
        self.btn_home_stage = self.main_window.btn_home_stage
        self.btn_move_to_pos = self.main_window.btn_move_to_pos
        self.le_pos_um = self.main_window.le_pos_um
        self.le_pos_fs = self.main_window.le_pos_fs
        self.lcd_current_pos_um = self.main_window.lcd_cnt_update_current_pos_um
        self.lcd_current_pos_fs = self.main_window.lcd_cnt_update_current_pos_fs
        self.lcd_current_pos_um_tab2 = self.main_window.lcd_tab2_current_pos_um
        self.lcd_current_pos_fs_tab2 = self.main_window.lcd_tab2_current_pos_fs
        self.btn_setT0 = self.main_window.btn_set_T0
        self.plot_window = plotf.PlotWindow(self.main_window.le_cont_upd_xmin,
                                            self.main_window.le_cont_upd_xmax,
                                            self.main_window.le_cont_upd_ymin,
                                            self.main_window.le_cont_upd_ymax,
                                            self.main_window.gv_cont_upd_spec)
        self.actionStop = self.main_window.actionStop

        # create a curve and add it to the plotwidget
        self.curve = plotf.create_curve()
        self.plot_window.plotwidget.addItem(self.curve)

        # initialize the step size and position, 0 is arbitrary
        self._step_size_fs = 0
        self._move_to_pos_fs = 0
        self._step_size_fs_spectrogram = 0

        # initialize the start and end position, 0 is arbitrary
        self._start_pos_fs = -100
        self._end_pos_fs = 100

        # the inputs have to be floats
        self.le_pos_fs.setValidator(qtg.QDoubleValidator())
        self.le_pos_um.setValidator(qtg.QDoubleValidator())
        self.le_step_size_fs.setValidator(qtg.QDoubleValidator())
        self.le_step_size_um.setValidator(qtg.QDoubleValidator())

        # allow the lcd to display decimals, and adjust a format setting so
        # the numbers don't show up faded.
        self.lcd_current_pos_fs.setSmallDecimalPoint(True)
        self.lcd_current_pos_fs.setSegmentStyle(qt.QLCDNumber.Flat)
        self.lcd_current_pos_um.setSmallDecimalPoint(True)
        self.lcd_current_pos_um.setSegmentStyle(qt.QLCDNumber.Flat)

        self.lcd_current_pos_fs_tab2.setSmallDecimalPoint(True)
        self.lcd_current_pos_fs_tab2.setSegmentStyle(qt.QLCDNumber.Flat)
        self.lcd_current_pos_um_tab2.setSmallDecimalPoint(True)
        self.lcd_current_pos_um_tab2.setSegmentStyle(qt.QLCDNumber.Flat)

        # connect and initialize
        self.connect()

        # update the display
        self.update_stepsize_from_le_fs()
        self.update_stepsize_spectrogram_from_le_fs()
        self.update_current_pos()

        self.update_startpos_from_le_fs()
        self.update_endpos_from_le_fs()

        # do runnables already exist
        self.cont_update_runnable_exists = False
        self.motor_runnable_exists = False

        # Error Popup Window
        self.error_window = ErrorWindow()

        # backlash distance: 3 micon
        # I believe it's rated to be <3 micron, so I think this should do it
        # maybe it's not needed at all...
        self.backlash = 3.0

        # step size limit
        self.step_size_max = 50.

    # I have create_runnable and connect_runnable defined separately because
    # every time the pool finishes it deletes the instance, so it needs to be
    # re-initialized every time
    def create_runnable(self, string):
        if string == "spectrum":
            self.runnable_update_spectrum = UpdateSpectrumRunnable(
                self.spectrometer)
        elif string == "motor":
            self.runnable_update_motor = UpdateMotorPositionRunnable(
                self.motor_interface)

    def connect_runnable(self, string):
        if string == 'spectrum':
            # for each retrieval of the spectrum update the plot in the gui
            self.runnable_update_spectrum.progress.connect(self.plot_update)

            # if the stop action button is pressed, stop the continuous update
            self.actionStop.triggered.connect(self.stop_continuous_update)
        elif string == "motor":
            # continuously update motor position
            self.runnable_update_motor.progress.connect(
                self.update_current_pos)

            # if the stop button is pushed, also stop the motor (in a
            # controlled manner)
            self.actionStop.triggered.connect(self.stop_motor)

            # signal when the motor is finished moving
            # when finished moving, update the current position one more time
            self.runnable_update_motor.finished.connect(self.motor_finished)
            self.runnable_update_motor.finished.connect(self.update_current_pos)

    def connect(self):
        # if the start continuous update button is pressed start the
        # continuous update
        self.btn_start.clicked.connect(self.start_continuous_update)

        # update step size (for both um and fs)
        self.le_step_size_um.editingFinished.connect(
            self.update_stepsize_from_le_um)
        self.le_step_size_fs.editingFinished.connect(
            self.update_stepsize_from_le_fs)
        self.le_step_size_um_tab2.editingFinished.connect(
            self.update_stepsize_spectrogram_from_le_um)
        self.le_step_size_fs_tab2.editingFinished.connect(
            self.update_stepsize_spectrogram_from_le_fs)

        # update move_to_pos (for both um and fs)
        self.le_pos_um.editingFinished.connect(
            self.update_move_to_pos_from_le_um)
        self.le_pos_fs.editingFinished.connect(
            self.update_move_to_pos_from_le_fs)

        # update start and end pos (for both um and fs)
        self.le_startpos_fs.editingFinished.connect(
            self.update_startpos_from_le_fs)
        self.le_startpos_um.editingFinished.connect(
            self.update_startpos_from_le_um)
        self.le_endpos_fs.editingFinished.connect(
            self.update_endpos_from_le_fs)
        self.le_endpos_um.editingFinished.connect(
            self.update_endpos_from_le_um)

        # connect the set T0 button
        self.btn_setT0.clicked.connect(self.set_T0)

        # connect the home stage button
        self.btn_home_stage.clicked.connect(self.home_stage)

        # connect the step left and step right buttons
        self.btn_step_left.clicked.connect(self.step_left)
        self.btn_step_right.clicked.connect(self.step_right)

        # connect the move_to_pos button (can connect to move_to_pos_um or
        # move_to_pos_fs)
        self.btn_move_to_pos.clicked.connect(self.move_to_pos)

        # connect the collect spectrogram button
        self.btn_collect_spectrogram.clicked.connect(self.collect_spectrogram)

    @property
    def T0_um(self):
        return self.motor_interface.T0_um

    @property
    def step_size_um(self):
        # set the step size in micron based off the step size in fs
        return T_fs_to_dist_um(self._step_size_fs)

    @property
    def step_size_fs(self):
        return self._step_size_fs

    @property
    def step_size_um_spectrogram(self):
        # set the step size in micron based off the step size in fs
        return T_fs_to_dist_um(self._step_size_fs_spectrogram)

    @property
    def step_size_fs_spectrogram(self):
        return self._step_size_fs_spectrogram

    @property
    def move_to_pos_fs(self):
        return self._move_to_pos_fs

    @property
    def move_to_pos_um(self):
        return T_fs_to_dist_um(self.move_to_pos_fs) + self.T0_um

    @T0_um.setter
    def T0_um(self, value_um):
        self.motor_interface.T0_um = value_um

    @move_to_pos_fs.setter
    def move_to_pos_fs(self, value_fs):
        self._move_to_pos_fs = value_fs

        # update the line edits
        self.update_move_to_pos_le_fs()
        self.update_move_to_pos_le_um()

    @move_to_pos_um.setter
    def move_to_pos_um(self, value_um):
        value_fs = dist_um_to_T_fs(value_um - self.T0_um)
        self.move_to_pos_fs = value_fs

        # update the line edits
        self.update_move_to_pos_le_fs()
        self.update_move_to_pos_le_um()

    @step_size_um.setter
    def step_size_um(self, value_um):
        # step_size_um is based off step_size_fs so just update step_size_fs
        self._step_size_fs = dist_um_to_T_fs(value_um)

        # update the line edits
        self.update_stepsize_le_um()
        self.update_stepsize_le_fs()

    @step_size_fs.setter
    def step_size_fs(self, value_fs):
        self._step_size_fs = value_fs

        # update the line edits
        self.update_stepsize_le_um()
        self.update_stepsize_le_fs()

    @step_size_um_spectrogram.setter
    def step_size_um_spectrogram(self, value_um):
        # step_size_um is based off step_size_fs so just update step_size_fs
        self._step_size_fs_spectrogram = dist_um_to_T_fs(value_um)

        # update the line edits
        self.update_stepsize_spectrogram_le_fs()
        self.update_stepsize_spectrogram_le_um()

    @step_size_fs_spectrogram.setter
    def step_size_fs_spectrogram(self, value_fs):
        self._step_size_fs_spectrogram = value_fs

        # update the line edits
        self.update_stepsize_spectrogram_le_um()
        self.update_stepsize_spectrogram_le_fs()

    @property
    def start_pos_fs(self):
        return self._start_pos_fs

    @start_pos_fs.setter
    def start_pos_fs(self, value):
        self._start_pos_fs = value

        # update the line edits
        self.update_startpos_le_fs()
        self.update_startpos_le_um()

    @property
    def start_pos_um(self):
        # I'm making it so that the start position in micron is defined
        # based off the start position in time
        return T_fs_to_dist_um(self.start_pos_fs) + self.T0_um

    @start_pos_um.setter
    def start_pos_um(self, value_um):
        # start_pos_um is taken from start_pos_fs
        # so just set start_pos_fs
        self.start_pos_fs = dist_um_to_T_fs(value_um - self.T0_um)

        # update the line edits
        self.update_startpos_le_fs()
        self.update_startpos_le_um()

    @property
    def end_pos_fs(self):
        return self._end_pos_fs

    @end_pos_fs.setter
    def end_pos_fs(self, value):
        self._end_pos_fs = value

        # update the line edits
        self.update_endpos_le_fs()
        self.update_endpos_le_um()

    @property
    def end_pos_um(self):
        # I'm making it so that the start position in micron is defined
        # based off the start position in time
        return T_fs_to_dist_um(self.end_pos_fs) + self.T0_um

    @end_pos_um.setter
    def end_pos_um(self, value_um):
        # end_pos_um is taken from end_pos_fs
        # so just set end_pos_fs
        self.end_pos_fs = dist_um_to_T_fs(value_um - self.T0_um)

        # update the line edits
        self.update_endpos_le_fs()
        self.update_endpos_le_um()

    def update_stepsize_from_le_um(self):
        step_size_um = float(self.le_step_size_um.text())
        self.step_size_um = step_size_um

    def update_stepsize_from_le_fs(self):
        step_size_fs = float(self.le_step_size_fs.text())
        self.step_size_fs = step_size_fs

    def update_stepsize_spectrogram_from_le_um(self):
        step_size_um = float(self.le_step_size_um_tab2.text())
        self.step_size_um_spectrogram = step_size_um

    def update_stepsize_spectrogram_from_le_fs(self):
        step_size_fs = float(self.le_step_size_fs_tab2.text())
        self.step_size_fs_spectrogram = step_size_fs

    def update_startpos_from_le_um(self):
        startpos_um = float(self.le_startpos_um.text())
        self.start_pos_um = startpos_um

    def update_startpos_from_le_fs(self):
        startpos_fs = float(self.le_startpos_fs.text())
        self.start_pos_fs = startpos_fs

    def update_endpos_from_le_um(self):
        endpos_um = float(self.le_endpos_um.text())
        self.end_pos_um = endpos_um

    def update_endpos_from_le_fs(self):
        endpos_fs = float(self.le_endpos_fs.text())
        self.end_pos_fs = endpos_fs

    def update_move_to_pos_from_le_um(self):
        move_to_pos_um = float(self.le_pos_um.text())
        self.move_to_pos_um = move_to_pos_um

    def update_move_to_pos_from_le_fs(self):
        move_to_pos_fs = float(self.le_pos_fs.text())
        self.move_to_pos_fs = move_to_pos_fs

    def update_stepsize_le_um(self):
        self.le_step_size_um.setText('%.3f' % self.step_size_um)

    def update_stepsize_le_fs(self):
        self.le_step_size_fs.setText('%.3f' % self.step_size_fs)

    def update_stepsize_spectrogram_le_um(self):
        self.le_step_size_um_tab2.setText(
            '%.3f' % self.step_size_um_spectrogram)

    def update_stepsize_spectrogram_le_fs(self):
        self.le_step_size_fs_tab2.setText(
            '%.3f' % self.step_size_fs_spectrogram)

    def update_startpos_le_um(self):
        self.le_startpos_um.setText('%.3f' % self.start_pos_um)

    def update_startpos_le_fs(self):
        self.le_startpos_fs.setText('%.3f' % self.start_pos_fs)

    def update_endpos_le_um(self):
        self.le_endpos_um.setText('%.3f' % self.end_pos_um)

    def update_endpos_le_fs(self):
        self.le_endpos_fs.setText('%.3f' % self.end_pos_fs)

    def update_move_to_pos_le_um(self):
        self.le_pos_um.setText('%.5f' % self.move_to_pos_um)

    def update_move_to_pos_le_fs(self):
        self.le_pos_fs.setText('%.5f' % self.move_to_pos_fs)

    def start_continuous_update(self):
        # I would like to have the start_continuous_update button
        # work like a toggle. So, if the runnable already exists, then
        # just stop the process and return.
        if self.cont_update_runnable_exists:
            self.stop_continuous_update()
            return

        self.cont_update_runnable_exists = True

        self.btn_start.setText("Stop \n Continuous Update")

        # create a runnable instance and connect the relevant signals and slots
        self.create_runnable('spectrum')
        self.connect_runnable('spectrum')

        # start the continuous update
        pool.start(self.runnable_update_spectrum)

    def stop_continuous_update(self):
        # stop the continuous update
        self.runnable_update_spectrum.stop()
        self.cont_update_runnable_exists = False

        self.btn_start.setText("Start \n Continuous Update")

    def plot_update(self, X):
        # the signal should emit wavelengths and intensities
        wavelengths, intensities = X
        # set the data to the new spectrum
        self.curve.setData(x=wavelengths, y=intensities)

    def step_right(self):
        # if motor is currently moving, just stop the motor.
        if self.motor_runnable_exists:
            self.stop_motor()
            return

        # set a limit on the step size to be 50 fs
        if self.step_size_fs > self.step_size_max:
            raise_error(self.error_window, "step size cannot exceed 50 fs")
            return

        exceed = self.motor_interface.value_exceeds_limits(self.step_size_um)
        if not exceed:
            self.motor_interface.move_by_um(self.step_size_um)
            self.update_current_pos()
        else:
            return

    def step_left(self):
        # if motor is currently moving, just stop the motor.
        if self.motor_runnable_exists:
            self.stop_motor()
            return

        # set a limit on the step size to be 50 fs
        if self.step_size_fs > self.step_size_max:
            raise_error(self.error_window, "step size cannot exceed 50 fs")
            return

        exceed = self.motor_interface.value_exceeds_limits(-self.step_size_um)
        if not exceed:
            self.motor_interface.move_by_um(-self.step_size_um)
            self.update_current_pos()
        else:
            return

    def move_to_pos(self, target_um=False):

        # I would like to have the move_to_pos button
        # work like a toggle. So, if the runnable already exists, then
        # just stop the process and return.
        if self.motor_runnable_exists:
            # raise_error(self.error_window, "stop the motor first!")
            # return
            self.stop_motor()
            return

        if not target_um:
            target_um = self.move_to_pos_um

        exceed = self.motor_interface.value_exceeds_limits(
            target_um - self.motor_interface.pos_um)
        if not exceed:
            self.motor_runnable_exists = True
            self.btn_move_to_pos.setText("stop motion")

            self.motor_interface.pos_um = target_um

            # create a runnable instance and connect the relevant signals and
            # slots
            self.create_runnable('motor')
            self.connect_runnable('motor')

            pool.start(self.runnable_update_motor)
        else:
            return

    def update_current_pos(self):
        self.lcd_current_pos_um.display('%.3f' % self.motor_interface.pos_um)
        self.lcd_current_pos_fs.display('%.3f' % self.motor_interface.pos_fs)

        self.lcd_current_pos_um_tab2.display(
            '%.3f' % self.motor_interface.pos_um)
        self.lcd_current_pos_fs_tab2.display(
            '%.3f' % self.motor_interface.pos_fs)

    def stop_motor(self):
        self.runnable_update_motor.stop()
        self.motor_runnable_exists = False

        self.btn_move_to_pos.setText("move to position")

    def motor_finished(self):
        self.motor_runnable_exists = False
        self.btn_move_to_pos.setText("move to position")
        # print("motor finished moving!")

    def set_T0(self):
        # I think this ought to do it
        self.T0_um = self.motor_interface.pos_um
        self.move_to_pos_fs = 0
        self.update_current_pos()

        self.update_startpos_from_le_fs()
        self.update_endpos_from_le_fs()

    def home_stage(self):
        # I would like to have the home_stage button
        # work like a toggle. So, if the runnable already exists, then
        # just stop the process and return.
        if self.motor_runnable_exists:
            # raise_error(self.error_window, "stop the motor first!")
            # return
            self.stop_motor()
            return

        self.motor_runnable_exists = True

        self.motor_interface.motor.home_motor(blocking=False)

        self.create_runnable('motor')
        self.connect_runnable('motor')
        pool.start(self.runnable_update_motor)

    # TODO I think this is the last thing remaining for you to do
    def collect_spectrogram(self):
        """
        I've spent some time thinking about this, and I think I'll just do
        the move stop method for now. Ideally in the future it would
        be good to implement continuous scanning, and sync the stage motion
        with the spectrometer's data acquisition via a trigger sent
        from the stage to the spectrometer.
        """

        # I'm assuming the only thing that can take a while is moving to the
        # start position.
        def move_to_start():
            self.move_to_pos(self.start_pos_um)

        self.move_to_pos(self.start_pos_um - self.backlash)
        self.runnable_update_motor.finished.connect(move_to_start)


class CollectSpectrogramRunnable(qtc.QRunnable):
    def __init__(self, motor_interface, spectrometer, end_um, step_um):
        super().__init__()

        motor_interface: MotorInterface
        spectrometer: util.Spectrometer
        self.motor_interface = motor_interface
        self.spectrometer = spectrometer
        self.signal = Signal()
        self.started = self.signal.started
        self.progress = self.signal.progress
        self.finished = self.signal.finished

        self.end_um = end_um
        self.step_um = step_um

        self._stop = False

    def stop(self):
        self._stop = True

    def run(self):
        while self.motor_interface.pos_um < self.end_um:

            # if stop has been set to true, then stop
            if self._stop:
                self._stop = False
                return

            # acquire spectrum
            wavelengths, intensities = self.spectrometer.get_spectrum()

            # emit current position in time, and the spectrum (wavelengths,
            # spectrum)
            self.progress.emit(self.motor_interface.pos_fs, wavelengths,
                               intensities)

            # step the motor
            self.motor_interface.move_by_um(self.step_um)

            # TODO right now this is just so the GUI doesn't freeze up,
            #  you should remember to remove this for the actual program
            time.sleep(.001)


class UpdateMotorPositionRunnable(qtc.QRunnable):
    def __init__(self, motor_interface):
        super().__init__()

        motor_interface: MotorInterface
        self.motor_interface = motor_interface
        self.signal = Signal()
        self.started = self.signal.started
        self.progress = self.signal.progress
        self.finished = self.signal.finished

        self.event_finished = threading.Event()

    def stop(self):
        self.motor_interface.motor.stop_motor()

    def run(self):
        while self.motor_interface.motor.is_in_motion:
            self.progress.emit(None)
            time.sleep(.001)

        self.finished.emit(None)
        self.event_finished.set()


class UpdateSpectrumRunnable(qtc.QRunnable):
    """Runnable class for the ContinuousUpdate class"""

    def __init__(self, spectrometer):
        super().__init__()

        # this class takes as input the spectrometer which it will
        # continuously pull the the spectrum from
        spectrometer: util.Spectrometer
        self.spectrometer = spectrometer
        # also initialize a signal so you can transmit the spectrum to the
        # main Continuous Update class
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
        # while stop is false, continuously get the spectrum
        while not self._stop:
            # get the spectrum
            wavelengths, intensities = self.spectrometer.get_spectrum()
            # emit the spectrum as a signal
            self.progress.emit([wavelengths, intensities])

            # TODO I don't know how fast it does this, so I'm telling it to
            #  sleep for .001 seconds. If it turns out that it already takes
            #  ~.001s to get the spectrum then you can delete this
            time.sleep(.001)


if __name__ == '__main__':
    app = qt.QApplication([])
    gui = MainWindow()
    app.exec()
