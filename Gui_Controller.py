import PyQt5.QtWidgets as qt
import PyQt5.QtCore as qtc
from Window import Ui_MainWindow

# will be used later on for continuous update
pool = qtc.QThreadPool.globalInstance()


class MainWindow(qt.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.show()


if __name__ == '__main__':
    app = qt.QApplication([])
    gui = MainWindow()
    app.exec()
