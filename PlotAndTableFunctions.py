"""This file should handle all the customized plotting and table widgets"""

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
        self.ymin, self.ymax = 0., 1.

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

    def set_ymin(self, ymin):
        self.setYRange(ymin, self.ymax)
        self.ymin = ymin

    def set_ymax(self, ymax):
        self.setYRange(self.ymin, ymax)
        self.ymax = ymax


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

        self.connect()

    @property
    def ymax(self):
        return self.plotwidget.ymax

    @ymax.setter
    def ymax(self, ymax):
        self.plotwidget.set_ymax(ymax)

    @property
    def ymin(self):
        return self.plotwidget.ymin

    @ymin.setter
    def ymin(self, ymin):
        self.plotwidget.set_ymin(ymin)

    @property
    def xmax(self):
        return self.plotwidget.xmax

    @xmax.setter
    def xmax(self, xmax):
        self.plotwidget.set_xmax(xmax)

    @property
    def xmin(self):
        return self.plotwidget.xmin

    @xmin.setter
    def xmin(self, xmin):
        self.plotwidget.set_xmin(xmin)

    def update_xmax(self):
        xmax = float(self.le_wl_ul.text())
        self.xmax = xmax

    def update_xmin(self):
        xmin = float(self.le_wl_ll.text())
        self.xmin = xmin

    def update_ymax(self):
        ymax = float(self.le_ul.text())
        self.ymax = ymax

    def update_ymin(self):
        ymin = float(self.le_ll.text())
        self.ymin = ymin

    def connect(self):
        self.le_ul.editingFinished.connect(self.update_ymax)
        self.le_ll.editingFinished.connect(self.update_ymin)
        self.le_wl_ul.editingFinished.connect(self.update_xmax)
        self.le_wl_ll.editingFinished.connect(self.update_xmin)

    def update_line_edits_to_properties(self):
        self.le_ll.setText('%.3f' % self.ymin)
        self.le_ul.setText('%.3f' % self.ymax)
        self.le_wl_ll.setText('%.3f' % self.xmin)
        self.le_wl_ul.setText('%.3f' % self.xmax)

    def format_to_current_viewBox(self):
        rect = self.plotwidget.viewRect()
        self.xmin, self.xmax = rect.left(), rect.right()
        self.ymin, self.ymax = rect.bottom(), rect.top()
        self.update_line_edits_to_properties()

    def format_to_curve(self, curve):
        curve: pg.PlotDataItem
        self.xmin, self.xmax = curve.xData[[0, -1]]
        self.ymin, self.ymax = curve.yData[[0, -1]]
        self.update_line_edits_to_properties()
