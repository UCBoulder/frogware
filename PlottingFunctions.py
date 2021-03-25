import pyqtgraph as pg
import PyQt5.QtWidgets as qt


class PlotWidget(pg.PlotWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.setBackground('w')
        self.getAxis('left').setPen('k')
        self.getAxis('bottom').setPen('k')
        self.getAxis('left').setTextPen('k')
        self.getAxis('bottom').setTextPen('k')

        self.xmin, self.xmax = 0., 1.

    def set_xlabel(self, label):
        self.getAxis('bottom').setLabel(label)

    def set_ylabel(self, label):
        self.getAxis('left').setLabel(label)

    def set_xmin(self, xmin):
        self.setXRange(xmin, self.xmax)
        self.xmin = xmin

    def set_xmax(self, xmax):
        self.setXRange(self.xmin, xmax)
        self.xmax = xmax


def create_curve(color='b', width=2, x=None, y=None):
    curve = pg.PlotDataItem(pen=pg.mkPen(color=color, width=width))
    if (x is not None) and (y is not None):
        curve.setData(x, y)
    return curve


class PlotWindow:
    def __init__(self, le_wl_ll, le_wl_ul, le_ll, le_ul, plotwidget):
        le_wl_ll: qt.QLineEdit
        le_wl_ul: qt.QLineEdit
        le_ll: qt.QLineEdit
        le_ul: qt.QLineEdit
        plotwidget: PlotWidget

        self.plotwidget = plotwidget
        self.le_wl_ll = le_wl_ll
        self.le_wl_ul = le_wl_ul
        self.le_ll = le_ll
        self.le_ul = le_ul
