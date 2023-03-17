from PyQt5 import QtWidgets, QtCore
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
import sys  # We need sys so that we can pass argv to QApplication
import os

import logging
logging.basicConfig()
logger = logging.getLogger("graph.py")
logger.setLevel(logging.DEBUG)

from data import plot_storage #Global variable in data.py

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.graphWidget = pg.PlotWidget()
        self.setCentralWidget(self.graphWidget)

        self.graphWidget.setBackground('#272822')

        #Put things that should be drawn from config in this little block
        self.colors = ['#F92672', '#66D9EF', '#A6E22E', '#FD971F']
        self.pens = [pg.mkPen(color = self.colors[i], width = 3) for i in range(len(self.colors))]
        self.numpens = 4
        self.wait_time = 50

        #Plot some dummy data once
        self.graph_ref = {0: self.graphWidget.plot([0], [0], pen = self.pens[0])}

        self._timer_init()

    def _timer_init(self):
        self.timer = QtCore.QTimer()
        self.timer.setInterval(self.wait_time)
        self.timer.timeout.connect(self.update_plot)
        self.timer.start()

    def update_plot(self):
        for line in range(plot_storage.get_num_lines()):
            new_x, new_y = plot_storage.get_line(line)
            if line in self.graph_ref.keys():
                self.graph_ref[line].setData(new_x, new_y, pen=self.pens[line%self.numpens])
            else:
                logger.debug("adding a new line to the plot")
                self.graph_ref[line] = self.graphWidget.plot(new_x, new_y, pen=self.pens[line%self.numpens])