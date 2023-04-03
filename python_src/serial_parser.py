#Grabs data from a serial connection
import serial
import time
import sys

import logging
logging.basicConfig()
logger = logging.getLogger("serial_parser.py")
logger.setLevel(logging.DEBUG)

from data import plot_storage

def screen_to_terminal():
    ser = serial.Serial(sys.argv[1], 19200)

    #Waits for the begin command
    while 1:
        begin = False
        while (not begin):
            try:
                string_line = ser.readline().decode().strip("\n").split(":")
            except UnicodeDecodeError:
                continue
            
            if(string_line[0] == "PLOTTER"):
                if (string_line[1] == "begin"):
                    begin = True

        restart = False
        while (not restart):
            try:
                string_line = ser.readline().decode().strip("\n").split(":")
            except UnicodeDecodeError:
                #Have to go back and wait for begin signal again
                restart = True
                continue

            if(string_line[0] == "PLOTTER"):
                if (string_line[1] == "add_line"):
                    #dispatch to a handler for add_line
                    pass

                elif(string_line[1] == "add_points"):
                    #should dispatch to a add_points handler
                    logger.debug(f"{time.time()} -> {string_line}")

def screen_to_data_storage(port_name):

    #Keyed on incoming descriptor, Value is plot_storage descriptor
    line_d_mapping = dict()

    ser = serial.Serial(port_name, 115200)

    while 1:

        #Waits for the begin command
        begin = False
        while (not begin):
            try:
                string_line = ser.readline().decode().strip("\n").split(":")
            except UnicodeDecodeError:
                continue
            
            if(string_line[0] == "PLOTTER"):
                if (string_line[1] == "begin"):
                    window_min = eval(string_line[2])
                    window_max = eval(string_line[3])

                    logger.debug(f"Set window min to {window_min}, and window_max to {window_max}")

                    if (window_min or window_max):
                        #Call some function that sets the window size
                        plot_storage.set_window_min_max(window_min, window_max)

                    begin = True

        #Goes until reset or exit
        restart = False
        while (not restart):

            if(plot_storage.kill_update_thread):
                logger.debug("Received kill.")
                sys.exit(0)

            try:
                string_line = ser.readline().decode().strip("\n").split(":")
                #logger.debug(string_line)
            except UnicodeDecodeError:
                #Have to go back and wait for begin signal again
                restart = True
                continue

            if(string_line[0] == "PLOTTER"):
                if (string_line[1] == "add_line"):
                    #Unpack the rest of the commands
                    incoming_descriptor = int(string_line[2])
                    x_fp_digits = int(string_line[3])
                    y_fp_digits = int(string_line[4])

                    line_d_mapping[incoming_descriptor] = plot_storage.add_line(x_fp_digits, y_fp_digits)

                    logger.debug(f"Added line to mapping. {line_d_mapping}")

                elif(string_line[1] == "add_points"):
                    #should dispatch to a add_points handler
                    storage_line_d = line_d_mapping[int(string_line[2])]
                    x_buffer = eval(string_line[3])
                    y_buffer = eval(string_line[4])

                    #logger.debug(storage_line_d)
                    #logger.debug(x_buffer)
                    #logger.debug(y_buffer)

                    plot_storage.add_points(x_buffer, y_buffer, storage_line_d)

                    logger.debug(f"Recv buffer at {time.time()}")

if __name__ == "__main__":
    #screen_to_terminal()
    logger.info("Serial Parser was run directly. Screening to (unused) data storage object.")
    screen_to_data_storage()