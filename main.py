from PyQt5 import QtWidgets, QtCore
import sys  # We need sys so that we can pass argv to QApplication
import os
from graph import MainWindow

import numpy as np
import time
import threading

from data import plot_storage

def dummy_update():
    while(1):
        plot_storage.add_point(time.time(), np.random.normal(10, 1))

        time.sleep(np.abs(np.random.normal(0.02, 0.01)))


def graph_main():

    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    update_thread = threading.Thread(target = dummy_update)

    update_thread.start()

    graph_main()