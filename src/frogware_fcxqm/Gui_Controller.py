# add these to path
import sys


#sys.path.append("hardware_comms/")

import PyQt5.QtWidgets as qt
import PyQt5.QtCore as qtc
from Window import Ui_MainWindow
import PlotAndTableFunctions as plotf
import numpy as np
from Error import Ui_Form
import PyQt5.QtGui as qtg
import gc
import threading
import python_phase_retrieval as pr
import scipy.integrate as scint
import matplotlib.pyplot as plt

from pylablib.devices.Thorlabs.kinesis import list_kinesis_devices 
from hardware_comms.ThorlabsKinesisMotor import ThorlabsKinesisMotor 
from hardware_comms.OceanOpticsSpectrometer import OceanOpticsSpectrometer 
from hardware_comms.device_interfaces import LinearMotor, Spectrometer, SpectrometerAverageException, StageOutOfBoundsException, StageLimitsNotSetException, SpectrometerIntegrationException
from hardware_comms.utilities import T_fs_to_dist_um, dist_um_to_T_fs
from seabreeze.spectrometers import Spectrometer as ooSpec


# will be used later on for any continuous update of the display that lasts more
# than a few seconds
pool = qtc.QThreadPool.globalInstance()

# global variables
tol_um = 0.1  # 100 nm
edge_limit_buffer_mm = 0.0  # 1 um
port = "COM34"

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
    This is the main GUI window.
    """

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.show()

        self.error_window = ErrorWindow()

        self.connect_motor_spectrometer()

        self.frog_land = FrogLand(self, self.motor, self.spectrometer)

        self.set_hardware_params()
        self.update_hardware_from_table_int_time()
        self.update_hardware_from_table_scans_to_avg()

        self.connect_signals()

    def closeEvent(self, *args):
        # self.continuous_update_tab.stop
        print("Frogging has stopped")
        self.frog_land.stop_all_runnables()

    '''
    Connect specific motor/spectrometer objects. Must implement
    the LinearMotor/Spectrometer interface
    '''
    def connect_motor_spectrometer(self):
        self.motor = ThorlabsKinesisMotor(list_kinesis_devices[0][0])
        self.motor.travel_limits_um = (0, 25e6)
        self.spectrometer = OceanOpticsSpectrometer(ooSpec.from_first_available())

    def connect_signals(self):
        self.tableWidget.cellChanged.connect(self.slot_for_tablewidget)
        self.tableWidget.cellClicked.connect(self.save_table_item)
        self.actionSave.triggered.connect(self.save_spectrogram)

        self.btn_plot_autocorrelation.clicked.connect(
            self.plot_intensity_autocorrelation
        )

    def set_hardware_params(self):
        # set integration time limits (obtained in microsecond from
        # the spectrometer)
        (
            int_time_lower_limit_us,
            int_time_upper_limit_us,
        ) = self.spectrometer.integration_time_micros_limit

        item_ll = qt.QTableWidgetItem()
        item_ul = qt.QTableWidgetItem()

        item_ll.setText(str(int_time_lower_limit_us * 1e-3))
        item_ul.setText(str(int_time_upper_limit_us * 1e-3))

        self.tableWidget.setItem(0, 1, item_ll)
        self.tableWidget.setItem(0, 2, item_ul)

    def update_table_from_hardware_int_time(self):
        # update the gui based off the hardware
        self.tableWidget.item(0, 0).setText(str(self.spectrometer.integration_time_micros * 1e-3))

    def update_hardware_from_table_int_time(self):
        self.spectrometer.integration_time_micros = float(self.tableWidget.item(0, 0).text()) * 1e3

    def update_hardware_from_table_scans_to_avg(self):
        self.spectrometer.scans_to_avg = int(self.tableWidget.item(1, 0).text())

    def save_table_item(self, row, col):
        self.saved_table_item_text = self.tableWidget.item(row, col).text()

    def slot_for_tablewidget(self, row, col):
        if (row, col) == (0, 0):
            if self.frog_land.spectrogram_now_running:
                raise_error(self.error_window, "stop spectrogram collection first")

                self.tableWidget.item(row, col).setText(self.saved_table_item_text)
                return

            if self.frog_land.cont_update_runnable_exists.is_set():
                raise_error(self.error_window, "stop spectrum update first")

                self.tableWidget.item(row, col).setText(self.saved_table_item_text)
                return

            try:
                int_time_ms = float(self.tableWidget.item(row, col).text())
                self.spectrometer.integration_time_micros = int_time_ms * 1e3 
                self.update_hardware_from_table_int_time()
            except SpectrometerIntegrationException as e:
                raise_error(self.error_window, e.message)
                self.tableWidget.item(row, col).setText(self.saved_table_item_text)

        if (row, col) == (0, 1) or (row, col) == (0, 2):
            raise_error(self.error_window, "Cannot edit this hardware setting")
            self.tableWidget.item(row, col).setText(self.saved_table_item_text)

        if (row, col) == (0, 3):
            raise_error(self.error_window, "I'm too lazy to let you change this")
            self.tableWidget.item(row, col).setText(self.saved_table_item_text)

        if (row, col) == (1, 0):
            if self.frog_land.spectrogram_now_running:
                raise_error(self.error_window, "stop spectrogram collection first")
                self.tableWidget.item(row, col).setText(self.saved_table_item_text)
                return

            if self.frog_land.cont_update_runnable_exists.is_set():
                raise_error(self.error_window, "stop spectrum update first")
                self.tableWidget.item(row, col).setText(self.saved_table_item_text)
                return

            scns_to_avg = float(self.tableWidget.item(row, col).text())

            if scns_to_avg % 1 != 0: 
                scns_to_avg = int(scns_to_avg)
                self.tableWidget.item(row, col).setText(str(scns_to_avg))

            try:
                self.update_hardware_from_table_scans_to_avg()

            except SpectrometerAverageException as e:
                raise_error(self.error_window, e.message)
                self.tableWidget.item(row, col).setText(self.saved_table_item_text)


    def format_data_to_save(self):
        if self.frog_land.spectrogram_array is None:
            raise_error(self.error_window, "No spectrogram has been collected yet")
            return

        data = self.frog_land.spectrogram_array
        to_vstack = self.frog_land.wl_axis
        to_hstack = self.frog_land.Taxis_fs
        _ = np.hstack((to_hstack[:, np.newaxis], data))
        top_row = np.hstack((np.array([np.nan]), to_vstack))
        final = np.vstack((top_row, _))
        return final

    def save_spectrogram(self):
        if self.frog_land.spectrogram_array is None:
            raise_error(self.error_window, "No spectrogram has been collected yet")
            return

        filename, _ = qt.QFileDialog.getSaveFileName(self, "Save Spectrogram")
        if filename == "":
            return

        filename: str
        if filename.lower()[-4:] != ".txt":
            if filename.lower()[-4:] == ".csv":
                raise_error(self.error_window, "only .txt format is supported :(")
                return
            filename += ".txt"

        final = self.format_data_to_save()
        np.savetxt(filename, final)

    def plot_intensity_autocorrelation(self):
        if self.frog_land.spectrogram_array is None:
            raise_error(self.error_window, "No spectrogram has been collected yet")
            return

        data = self.format_data_to_save()
        ret = pr.Retrieval()
        ret.load_data("hello world", spectrogram=data)
        s = ret.spectrogram
        autocorrelation = scint.simpson(s, x=ret.F_THz[::-1], axis=1)
        fig, ax = plt.subplots(1, 1, num="intensity autocorrelation")
        ax.plot(ret.T_fs, autocorrelation, ".-")
        fig.show()


class FrogLand:
    """
    This class is the main user interface. It expects an instance of
    MainWindow, LinearMotor, and Spectrometer class in the init
    function.
    """

    def __init__(self, main_window: MainWindow, motor: LinearMotor, spectrometer: Spectrometer):
        self.main_window = main_window
        self.spectrometer = spectrometer
        self.motor = motor

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
        self.plot1d_window = plotf.PlotWindow(
            self.main_window.le_cont_upd_xmin,
            self.main_window.le_cont_upd_xmax,
            self.main_window.le_cont_upd_ymin,
            self.main_window.le_cont_upd_ymax,
            self.main_window.gv_cont_upd_spec,
        )
        self.plot2d_window = plotf.PlotWindow(
            self.main_window.le_spectrogram_xmin,
            self.main_window.le_spectrogram_xmax,
            self.main_window.le_spectrogram_ymin,
            self.main_window.le_spectrogram_ymax,
            self.main_window.gv_Spectrogram,
        )
        self.actionStop = self.main_window.actionStop
        self.btn_set_ambient = self.main_window.btn_set_ambient
        self.btn_zero_ambient = self.main_window.btn_zero_ambient

        # create a curve and add it to the plotwidget
        self.curve = plotf.create_curve()
        self.plot1d_window.plotwidget.addItem(self.curve)

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

        # spectrogram collection
        self.spectrogram_collection_instance = CollectSpectrogram(self)

        # connect and initialize
        self.connect()

        # curr_mot_pos_um will be set by update_current_pos, so initialize it
        # here
        self._curr_mot_pos_um = None

        # update the display
        self.update_stepsize_from_le_fs()
        self.update_stepsize_spectrogram_from_le_fs()
        self.update_current_pos(self.motor.pos_um)

        self.update_startpos_from_le_fs()
        self.update_endpos_from_le_fs()

        self.set_T0(T0_um=self.read_T0_from_file())

        # do runnables already exist
        self.cont_update_runnable_exists = threading.Event()
        self.cont_update_loop_exited = threading.Event()
        self.motor_runnable_exists = threading.Event()

        # Error Popup Window
        self.error_window = ErrorWindow()

        # step size limit
        # self.step_size_max = 50.
        self.step_size_max = np.inf

        self.spectrogram_array = None
        self.Taxis_fs = None
        self.spectrogram_now_running = False

        self.ambient_intensity = np.zeros(len(self.spectrometer.wavelengths()))
        self.intensities = np.zeros(len(self.spectrometer.wavelengths()))
        self.bckgnd_subtrd = np.zeros(len(self.spectrometer.wavelengths()))

    # I have create_runnable and connect_runnable defined separately because
    # every time the pool finishes it deletes the instance, so it needs to be
    # re-initialized every time
    def create_runnable(self, string):
        if string == "spectrum":
            # set the continuous update spectrum flag to true
            # other parts of the program will need to check that
            # to know if the spectrometer is available
            self.cont_update_runnable_exists.set()
            self.cont_update_loop_exited.clear()

            # create a runnable
            self.runnable_update_spectrum = UpdateSpectrumRunnable(
                spectrometer=self.spectrometer,
                event_to_clear=self.cont_update_runnable_exists,
                event_to_set=self.cont_update_loop_exited,
            )

            # I don't know if this is necessary, but in case the old memory
            # is not freed up when re-assigning new content, do some garbage
            # collection
            gc.collect()
        elif string == "motor":
            # set the continuous motor update flag to true
            # other parts of the program will need to check that
            # to know if the motor is available
            self.motor_runnable_exists.set()

            # create a runnable
            self.runnable_update_motor = UpdateMotorPositionRunnable(
                motor=self.motor,
                event_to_clear=self.motor_runnable_exists,
            )

            # I don't know if this is necessary, but in case the old memory
            # is not freed up when re-assigning new content, do some garbage
            # collection
            gc.collect()

    def connect_runnable(self, string):
        """
        :param string: what runnable to connect: spectrum, motor

        You already take care in this program not to have more than one
        runnable instance for any hardware device running at one time.

        The only thing to make sure of is that you don't have "redundant
        retrieval", namely places where getting information of hardware
        is redundant and wastes time.
        """
        if string == "spectrum":
            # for each retrieval of the spectrum update the plot in the gui
            self.runnable_update_spectrum.progress.connect(self.plot_update)

            # if the stop action button is pressed, stop the continuous update
            self.actionStop.triggered.connect(self.stop_continuous_update)

        elif string == "motor":
            # continuously update motor position
            self.runnable_update_motor.progress.connect(self.update_current_pos)

            # if the stop button is pushed, also stop the motor (in a
            # controlled manner)
            self.actionStop.triggered.connect(self.stop_motor)

            # signal when the motor is finished moving
            # when finished moving, update the current position one more time
            self.runnable_update_motor.finished.connect(self.motor_finished)

    def connect(self):
        # if the start continuous update button is pressed start the
        # continuous update
        self.btn_start.clicked.connect(self.start_continuous_update)

        # update step size (for both um and fs)
        self.le_step_size_um.editingFinished.connect(self.update_stepsize_from_le_um)
        self.le_step_size_fs.editingFinished.connect(self.update_stepsize_from_le_fs)
        self.le_step_size_um_tab2.editingFinished.connect(
            self.update_stepsize_spectrogram_from_le_um
        )
        self.le_step_size_fs_tab2.editingFinished.connect(
            self.update_stepsize_spectrogram_from_le_fs
        )

        # update move_to_pos (for both um and fs)
        self.le_pos_um.editingFinished.connect(self.update_move_to_pos_from_le_um)
        self.le_pos_fs.editingFinished.connect(self.update_move_to_pos_from_le_fs)

        # update start and end pos (for both um and fs)
        self.le_startpos_fs.editingFinished.connect(self.update_startpos_from_le_fs)
        self.le_startpos_um.editingFinished.connect(self.update_startpos_from_le_um)
        self.le_endpos_fs.editingFinished.connect(self.update_endpos_from_le_fs)
        self.le_endpos_um.editingFinished.connect(self.update_endpos_from_le_um)

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

        # connect the set ambient and zero ambient buttons
        self.btn_set_ambient.clicked.connect(self.set_ambient)
        self.btn_zero_ambient.clicked.connect(self.zero_ambient)

        # connect the spectrogram collection instance
        self.spectrogram_collection_instance.signal.progress.connect(
            self.update_spectrogram_plot
        )
        self.spectrogram_collection_instance.signal.finished.connect(
            self.spectrogram_finished
        )
        self.actionStop.triggered.connect(self.spectrogram_collection_instance.stop)

    """The fact that the Spectrogram Collection is not run on a separate
    thread makes things slightly different.

    I found out that if you do not connect the signals in the Spectrogram
    Collection but instead do it in the Frogland class, then their
    slot functions are not called when the buttons are clicked. It appears
    this has to do with the fact that the SpectrogramCollection class
    is not executed on a separate thread.

    Lastly, if you leave the connections for these signals in this class,
    then there seems to be a conflict, where the buttons don't work
    although their slot functions are called when you click on them.

    As a result, I disconnect them here whenever running the spectrogram
    and re-connect them later."""

    def disconnect_for_spectrogram(self):
        # if the start continuous update button is pressed start the
        # continuous update
        self.btn_start.clicked.disconnect(self.start_continuous_update)

        # disconnect the home stage button
        self.btn_home_stage.clicked.disconnect(self.home_stage)

        # disconnect the step left and step right buttons
        self.btn_step_left.clicked.disconnect(self.step_left)
        self.btn_step_right.clicked.disconnect(self.step_right)

        # disconnect the move_to_pos button (can disconnect to move_to_pos_um or
        # move_to_pos_fs)
        self.btn_move_to_pos.clicked.disconnect(self.move_to_pos)

        # disconnect the collect spectrogram button
        self.btn_collect_spectrogram.clicked.disconnect(self.collect_spectrogram)

    def reconnect_for_spectrogram(self):
        # if the start continuous update button is pressed start the
        # continuous update
        self.btn_start.clicked.connect(self.start_continuous_update)

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

    def stop_all_runnables(self):
        if self.motor_runnable_exists.is_set():
            self.stop_motor()
        if self.cont_update_runnable_exists.is_set():
            self.stop_continuous_update()

    # @property
    # def curr_mot_pos_um(self):
    #     if self._curr_mot_pos_um is None:
    #         return self.motor.pos_um
    #     else:
    #         return self._curr_mot_pos_um

    # @curr_mot_pos_um.setter
    # def curr_mot_pos_um(self, value_um):
    #     self._curr_mot_pos_um = value_um

    # @property
    # def T0_um(self):
    #     return self.motor.T0_um

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

    # @property
    # def move_to_pos_fs(self):
    #     return self._move_to_pos_fs

    # @property
    # def move_to_pos_um(self):
    #     return T_fs_to_dist_um(self.move_to_pos_fs) + self.T0_um

    # @T0_um.setter
    # def T0_um(self, value_um):
    #     self.motor.T0_um = value_um

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
        self.le_step_size_um.setText("%.3f" % self.step_size_um)

    def update_stepsize_le_fs(self):
        self.le_step_size_fs.setText("%.3f" % self.step_size_fs)

    def update_stepsize_spectrogram_le_um(self):
        self.le_step_size_um_tab2.setText("%.3f" % self.step_size_um_spectrogram)

    def update_stepsize_spectrogram_le_fs(self):
        self.le_step_size_fs_tab2.setText("%.3f" % self.step_size_fs_spectrogram)

    def update_startpos_le_um(self):
        self.le_startpos_um.setText("%.3f" % self.start_pos_um)

    def update_startpos_le_fs(self):
        self.le_startpos_fs.setText("%.3f" % self.start_pos_fs)

    def update_endpos_le_um(self):
        self.le_endpos_um.setText("%.3f" % self.end_pos_um)

    def update_endpos_le_fs(self):
        self.le_endpos_fs.setText("%.3f" % self.end_pos_fs)

    def update_move_to_pos_le_um(self):
        self.le_pos_um.setText("%.5f" % self.move_to_pos_um)

    def update_move_to_pos_le_fs(self):
        self.le_pos_fs.setText("%.5f" % self.move_to_pos_fs)

    def start_continuous_update(self):
        # I would like to have the start_continuous_update button
        # work like a toggle. So, if the runnable already exists, then
        # just stop the process and return.
        if self.cont_update_runnable_exists.is_set():
            self.stop_continuous_update()
            return

        spectrum = self.spectrometer.spectrum()
        self.plot_update(spectrum)
        lims = np.array([0, max(spectrum[1])])
        self.plot1d_window.format_to_xy_data(self.spectrometer.wavelengths(), lims)

        self.btn_start.setText("Stop \n Continuous Update")

        # create a runnable instance and connect the relevant signals and slots
        self.create_runnable("spectrum")
        self.connect_runnable("spectrum")

        # start the continuous update
        pool.start(self.runnable_update_spectrum)

    def stop_continuous_update(self):
        # stop the continuous update
        self.runnable_update_spectrum.stop()

        # waiting for the loop to exit should be very fast, so we can
        # afford to wait, make sure to do this only after calling stop
        self.cont_update_loop_exited.wait()
        self.btn_start.setText("Start \n Continuous Update")

    def plot_update(self, X):
        # the signal should emit wavelengths and intensities, the spectrogram
        # signal will emit also an integer which we ignore here
        wavelengths, intensities, *_ = X
        self.intensities[:] = intensities[:]
        # set the data to the new spectrum
        self.bckgnd_subtrd = intensities - self.ambient_intensity
        self.bckgnd_subtrd = np.where(self.bckgnd_subtrd > 0.0, self.bckgnd_subtrd, 0.0)
        self.curve.setData(x=wavelengths, y=self.bckgnd_subtrd)

    def set_ambient(self):
        self.ambient_intensity[:] = self.intensities[:]

    def zero_ambient(self):
        self.ambient_intensity[:] = 0.0

    def step_right(self, *args, step_size_um=None, ignore_spectrogram=False):
        # if step_size_um is not specified, then step according
        # to the step size in the first tab
        if step_size_um is None:
            step_size_um = self.step_size_um

        # if motor is currently moving, just stop the motor.
        if self.motor_runnable_exists.is_set():
            self.motor.stop_motor(blocking=True)
            return

        # set a limit on the step size to be ... fs
        if self.step_size_fs > self.step_size_max:
            raise_error(self.error_window, "step size cannot exceed 50 fs")
            return
        #TODO I don't understand this one yet
        try:
            self.motor.move_by_um(step_size_um)

            self.create_runnable("motor")
            self.connect_runnable("motor")
            pool.start(self.runnable_update_motor)
        except:
            return

    def step_left(self, *args, step_size_um=None, ignore_spectrogram=False):
        # if step_size_um is not specified, then step according
        # to the step size in the first tab
        if step_size_um is None:
            step_size_um = self.step_size_um

        # if motor is currently moving, just stop the motor.
        if self.motor_runnable_exists.is_set():
            self.motor.stop_motor(blocking=True)
            return

        # set a limit on the step size to be ... fs
        if self.step_size_fs > self.step_size_max:
            raise_error(self.error_window, "step size cannot exceed 50 fs")
            return

        exceed = self.motor.value_exceeds_limits(-step_size_um)
        if not exceed:
            self.motor.move_by_um(-step_size_um)

            self.create_runnable("motor")
            self.connect_runnable("motor")
            pool.start(self.runnable_update_motor)
        else:
            return

    def move_to_pos(self, target_um=False):
        # if motor is currently moving, just stop the motor.
        if self.motor_runnable_exists.is_set():
            self.stop_motor()
            return

        if not target_um:
            target_um = self.move_to_pos_um

        # only retrieve the position once!
        motor_pos_um = self.curr_mot_pos_um
        exceed = self.motor.value_exceeds_limits(target_um - motor_pos_um)
        if not exceed:
            self.btn_move_to_pos.setText("stop motion")

            self.motor.pos_um = target_um

            # create a runnable instance and connect the relevant signals and
            # slots
            self.create_runnable("motor")
            self.connect_runnable("motor")
            pool.start(self.runnable_update_motor)
        else:
            return

    def update_current_pos(self, pos_um):
        self.curr_mot_pos_um = pos_um
        motor_pos_fs = dist_um_to_T_fs(pos_um - self.motor.T0_um)
        self.lcd_current_pos_um.display("%.3f" % pos_um)
        self.lcd_current_pos_fs.display("%.3f" % motor_pos_fs)

        self.lcd_current_pos_um_tab2.display("%.3f" % pos_um)
        self.lcd_current_pos_fs_tab2.display("%.3f" % motor_pos_fs)

    """
    The motor takes a while to stop (it slows to a stop). Using a wait() flag
    may cause the GUI to freeze, so instead of using a threading Event, I just
    connect a finished signal to the motor_finished slot
    """

    # stop_motor should send the stop_signal to the motor hardware
    # it will not set motor_runnable_exists to False, that will only
    # occur once is_in_motion is detected to be False
    def stop_motor(self):
        # if you already tried stopping the motor, do nothing (the motor
        # is already in the process of stopping)
        if self.runnable_update_motor._stop_initiated:
            return

        # otherwise, stop the motor
        else:
            self.runnable_update_motor.stop()

    # this is connected only to the motor runnable's finished signal
    # that is emitted when is_in_motion is detected to be false.
    # it sets motor_runnable_exists to False, and does some house keeping
    # with button labels
    def motor_finished(self):
        self.btn_move_to_pos.setText("move to position")
        self.btn_home_stage.setText("home stage")

    def set_T0(self, *args, T0_um=None):
        if T0_um is None:
            # read the motor position
            motor_pos_um = self.curr_mot_pos_um

            # set T0 position to current motor position
            self.T0_um = motor_pos_um

            # write the new T0 to file
            self.write_T0_to_file(self.T0_um)

        else:
            # set T0 position to current motor position
            self.T0_um = T0_um

            # read the motor position
            motor_pos_um = self.curr_mot_pos_um

        # set the move to position to 0
        self.move_to_pos_fs = 0

        # update the line edits
        self.update_current_pos(motor_pos_um)
        self.update_startpos_from_le_fs()
        self.update_endpos_from_le_fs()

    def read_T0_from_file(self):
        return np.loadtxt("T0_um.txt")

    def write_T0_to_file(self, T0_um):
        with open("T0_um.txt", "w") as file:
            file.write(str(T0_um))

    def home_stage(self):
        # if motor is currently moving, just stop the motor.
        if self.motor_runnable_exists.is_set():
            self.stop_motor()
            return

        self.motor.home(blocking=False)

        self.create_runnable("motor")
        self.connect_runnable("motor")
        pool.start(self.runnable_update_motor)

        self.btn_home_stage.setText("stop homing")

        # it takes a sec for the motor to start moving when homing,
        # so you to prevent an immediate motor finished flag, let it get going
        # first.
        # time.sleep(.1)

    def collect_spectrogram(self, *args):
        # if motor is in motion, stop the motor
        if self.motor_runnable_exists.is_set():
            self.stop_motor()
            return

        # we need access to the spectrometer, so stop the spectrum update but
        # we're just stopping it (don't return). Because the continuous
        # spectrum update loop is run on a different thread, you need to
        # let the current loop finish before continuing to grab a spectrum.
        # This is implemented using a threading event
        if self.cont_update_runnable_exists.is_set():
            self.stop_continuous_update()

        self.move_to_pos(self.start_pos_um)
        self.runnable_update_motor.finished.connect(self._check_if_at_start)

    def spectrogram_finished(self):
        self.spectrogram_now_running = False
        self.btn_collect_spectrogram.setText("Collect \n Spectrogram")
        self.reconnect_for_spectrogram()

    def _start_spectrogram_collection(self):
        self.spectrogram_now_running = True
        self.spectrogram_collection_instance.start()

    def _check_if_at_start(self):
        if abs(self.curr_mot_pos_um - self.start_pos_um) > tol_um:
            return

        else:
            self._prep_spectrogram()
            self._start_spectrogram_collection()

    def _prep_spectrogram(self):
        if np.all(self.intensities == 0):
            X = self.spectrometer.spectrum()
            self.plot_update(X)
            lims = np.array([0, max(self.intensities)])
            self.plot1d_window.format_to_xy_data(self.spectrometer.wavelengths(), lims)

        self.btn_collect_spectrogram.setText("Stop \n Collection")

        self.Taxis_fs_list = []
        self.spectrogram_array_list = []

        self.plot2d_window.plotwidget.set_cmap("jet")

    def _setup_2dplot(self):
        self.wl_axis = self.spectrometer.wavelengths()
        self.plot2d_window.plotwidget.scale_axes(
            x=self.Taxis_fs, y=self.wl_axis, format="xy"
        )
        self.plot2d_window.format_to_xy_data(self.Taxis_fs, self.wl_axis)

    def update_spectrogram_plot(self, X):
        self.plot_update(X)
        wavelengths, intensities, n, pos_fs = X

        self.Taxis_fs_list.append(pos_fs)
        self.spectrogram_array_list.append(self.bckgnd_subtrd)

        self.Taxis_fs = np.array(self.Taxis_fs_list)
        self.spectrogram_array = np.array(self.spectrogram_array_list)

        self._setup_2dplot()

        self.plot2d_window.plotwidget.plot_image(self.spectrogram_array)


class CollectSpectrogram:
    def __init__(self, frogland: FrogLand):
        self.frogland = frogland
        self.motor = frogland.motor
        self.spectrometer = frogland.spectrometer

        self.signal = Signal()
        self.n = 0
        self._stop = False

    def connect_signals(self):
        self.frogland.btn_collect_spectrogram.clicked.connect(self.stop)
        self.frogland.btn_step_left.clicked.connect(self.stop)
        self.frogland.btn_step_right.clicked.connect(self.stop)
        self.frogland.btn_move_to_pos.clicked.connect(self.stop)
        self.frogland.btn_home_stage.clicked.connect(self.stop)
        self.frogland.btn_start.clicked.connect(self.stop)

    def disconnect_signals(self):
        self.frogland.btn_collect_spectrogram.clicked.disconnect(self.stop)
        self.frogland.btn_step_left.clicked.disconnect(self.stop)
        self.frogland.btn_step_right.clicked.disconnect(self.stop)
        self.frogland.btn_move_to_pos.clicked.disconnect(self.stop)
        self.frogland.btn_home_stage.clicked.disconnect(self.stop)
        self.frogland.btn_start.clicked.disconnect(self.stop)

    @property
    def step_um(self):
        return self.frogland.step_size_um_spectrogram

    @property
    def end_pos_um(self):
        return self.frogland.end_pos_um

    @property
    def end_pos_fs(self):
        return self.frogland.end_pos_fs

    def stop(self):
        if self.frogland.spectrogram_now_running:
            self._stop = True

        else:
            return

    def start(self):
        # re-initialize the spectrogram collection index
        self.n = 0

        self.frogland.disconnect_for_spectrogram()
        self.connect_signals()

        # begin the collection
        self.step_one()

    def emit_data(self, pos_um):
        # collect spectrum
        wavelengths, intensities = self.spectrometer.spectrum()

        """trying to average without detector saturation. Doesn't really help """
        # __________________________________________________________
        # N = 10
        # Intensities = np.zeros((N, len(intensities)))
        # Intensities[0] = intensities
        #
        # for i in range(1, N - 1, 1):
        #     Intensities[i] = self.spectrometer.get_spectrum()[1]
        #
        # intensities = np.mean(Intensities, 0)
        # __________________________________________________________

        pos_fs = dist_um_to_T_fs(pos_um - self.motor.T0_um)
        self.signal.progress.emit((wavelengths, intensities, self.n, pos_fs))

    def step_one(self):
        # check the stop flag, if it is true,
        # toggle it back to false and return
        if self._stop:
            self._stop = False
            self.disconnect_signals()
            self.signal.finished.emit(None)
            return

        # if we are not at the end of the spectrogram range
        # then collect a spectrum and step the motor
        else:
            pos_um = self.frogland.curr_mot_pos_um

            pos_fs = dist_um_to_T_fs(pos_um - self.motor.T0_um)
            print("point", self.n + 1, ", ", self.end_pos_fs - pos_fs, "fs remaining")

            self.emit_data(pos_um)

            if np.round(pos_um, 3) <= np.round(self.end_pos_um, 3):
                # step the motor
                self.frogland.step_right(
                    step_size_um=self.step_um, ignore_spectrogram=True
                )
                # connect motor finished flag to step_two
                self.frogland.runnable_update_motor.finished.connect(self.step_two)

            # otherwise, flag that the spectrogram collection is done
            else:
                self.disconnect_signals()
                self.signal.finished.emit(None)

    def step_two(self):
        # increment spectrogram collection index, and iterate again
        self.n += 1
        self.step_one()


class UpdateMotorPositionRunnable(qtc.QRunnable):
    def __init__(self, motor: LinearMotor, event_to_clear: threading.Event):
        super().__init__()

        self.motor = motor
        self.signal = Signal()
        self.started = self.signal.started
        self.progress = self.signal.progress
        self.finished = self.signal.finished

        self.event_to_clear = event_to_clear

    """
    I ran into an error where I believe the program was writing two
    messages to the port at the same time (get position, and stop). So,
    it's important to enforce sequential writing to the port. I'm doing that
    by putting the stop command in the run loop.
    """

    def stop(self):
        self.motor.stop(blocking=True)
    def run(self):

        #TODO may be broken. May need to read location from hardware
        while self.motor.is_in_motion():
            pos = self.motor.read_hw_pos_um()
            self.progress.emit(pos)
            # time.sleep(.001)

        # stop flag has been set to True, and the loop has terminated
        # clear the event
        self.event_to_clear.clear()

        pos = self.motor.read_hw_pos_um()
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
            wavelengths, intensities = self.spectrometer.spectrum()
            # emit the spectrum as a signal
            self.progress.emit([wavelengths, intensities])

        # stop flag has been set to True, and the loop has terminated
        # clear the event
        self.event_to_clear.clear()
        self.event_to_set.set()


if __name__ == "__main__":
    app = qt.QApplication([])
    gui = MainWindow()
    app.exec()
