from PyQt5 import QtWidgets, QtCore
import sys  # We need sys so that we can pass argv to QApplication
import os
from graph import MainWindow

import numpy as np
import time
import threading

import logging
logging.basicConfig()
logger = logging.getLogger("main.py")
logger.setLevel(logging.DEBUG)

from data import plot_storage

def dummy_update():
    motor = plot_storage.add_line()
    motor_smaller_noise = plot_storage.add_line()

    while(1):

        if(plot_storage.kill_update_thread):
            logger.debug("Received kill.")
            break

        curTime = time.time()
        plot_storage.add_point(curTime, np.sin(curTime) + np.random.normal(0, 0.1))
        plot_storage.add_point(curTime, np.sin(curTime), motor)
        plot_storage.add_point(curTime, np.sin(curTime) + np.random.normal(0, 0.05), motor_smaller_noise)

        time.sleep(np.abs(np.random.normal(0.02, 0.01)))

def graph_main():

    app = QtWidgets.QApplication(sys.argv)

    app.aboutToQuit.connect(plot_storage.cleanup)

    main = MainWindow()
    main.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    update_thread = threading.Thread(target = dummy_update)

    update_thread.start()

    graph_main()