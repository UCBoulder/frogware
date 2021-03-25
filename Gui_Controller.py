import PyQt5.QtWidgets as qt
import PyQt5.QtCore as qtc
from Window import Ui_MainWindow
import PlotAndTableFunctions as plotf
import numpy as np
import gc
import utilities as util

# will be used later on for any continuous update of the display that lasts more
# than a few seconds
pool = qtc.QThreadPool.globalInstance()

c_mks = 299792458


# Signal class to be used for Runnable
class Signal(qtc.QObject):
    started = qtc.pyqtSignal(object)
    progress = qtc.pyqtSignal(object)
    finished = qtc.pyqtSignal(object)


class MainWindow(qt.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.show()

        self.plot_cont_upd = plotf.PlotWindow(self.le_cont_upd_xmin, self.le_cont_upd_xmax, self.le_cont_upd_ymin,
                                              self.le_cont_upd_ymax, self.gv_cont_upd_spec)

        self.plot_spectrogram = plotf.PlotWindow(self.le_spectrogram_xmin, self.le_spectrogram_xmax,
                                                 self.le_spectrogram_ymin, self.le_spectrogram_ymax,
                                                 self.gv_Spectrogram)


class MotorInterface:
    def __init__(self, spectrometer, motor):
        spectrometer: util.Spectrometer
        motor: util.Motor
        self.spectrometer = spectrometer
        self.motor = motor

        self.T0_um = 0
        self._pos_um = 0
        self._pos_fs = 0

        self.pos_um = self.motor.position * 1e6  # assuming they give position in mks?

    @property
    def pos_um(self):
        return self._pos_um

    @property
    def pos_fs(self):
        return self._pos_fs

    @pos_um.setter
    def pos_um(self, value):
        self._pos_um = value
        self._pos_fs = (value - self.T0_um) * 1e9 / c_mks

    @pos_fs.setter
    def pos_fs(self, value):
        self._pos_fs = value
        self._pos_um = value * 1e-9 * c_mks + self.T0_um

    def connect(self):
        pass


if __name__ == '__main__':
    app = qt.QApplication([])
    gui = MainWindow()
    app.exec()
