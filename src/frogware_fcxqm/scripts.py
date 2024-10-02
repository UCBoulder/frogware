from .gui_controller import MainWindow
from PyQt5.QtWidgets import QApplication
import sys


def frogware():
    app = QApplication(sys.argv)
    gui = MainWindow()
    gui.show()
    sys.exit(app.exec())
