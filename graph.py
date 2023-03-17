from PyQt5 import QtWidgets, QtCore
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
import sys  # We need sys so that we can pass argv to QApplication
import os

from data import plot_storage #Global variable in data.py

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.graphWidget = pg.PlotWidget()
        self.setCentralWidget(self.graphWidget)

        #Put things that should be drawn from config in this little block
        self.pen = pg.mkPen(color = 'r', width = 3)
        self.wait_time = 50

        #Plot some dummy data once
        self.graph_ref = self.graphWidget.plot([0], [0], pen = self.pen)

        self._timer_init()

    def _timer_init(self):
        self.timer = QtCore.QTimer()
        self.timer.setInterval(self.wait_time)
        self.timer.timeout.connect(self.update_plot)
        self.timer.start()

    def update_plot(self):
        #Where to draw this from... global variable in data.py!
        new_x, new_y = plot_storage.get_line()
        self.graph_ref.setData(new_x, new_y, pen = self.pen)