#Grabs data from a serial connection
import serial
import time
import sys

import logging
logging.basicConfig()
logger = logging.getLogger("serial_parser.py")
logger.setLevel(logging.DEBUG)

if __name__ == "__main__":
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