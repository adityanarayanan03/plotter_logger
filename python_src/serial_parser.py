#Grabs data from a serial connection
import serial
import time

ser = serial.Serial('/dev/tty.usbserial-14220', 19200)

while 1:
    string_line = ser.readline().decode().strip("\n").split(":")
    if(string_line[0] == "PLOTTER"):
        if (string_line[1] == "add_line"):
            #dispatch to a handler for add_line
        elif(string_line[1] == "add_points"):
            #should dispatch to a add_points handler
            print(f"{time.time()} -> {string_line[2]}")
