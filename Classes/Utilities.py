"""
    Utilities for the SDNode project
    By: JOR
    v0.1 12APR14    Initial test, uses separate classes for send and receive
    v0.2 13APR14    Single class, threading within the class, line oriented
    v0.3 10JUL18    Recoded for Python 3.x
    v0.4 23MAY20    Added logfile utility and timestamp maker
"""

import socket
import time


def find_local_ipv4():
    local_host_ip = str(socket.gethostbyname(socket.gethostname()))
    if local_host_ip == '127.0.0.1':
        print("You must set the hostname correctly in /etc/hosts!")
        print("Existing until you sort this!!")
        exit(0)
    return local_host_ip


def return_local_time():
    local_time = time.localtime()  # get struct_time
    time_string = time.strftime("%H:%M:%S", local_time)
    return time_string


def seconds_later(event, how_many_seconds):
    return event + how_many_seconds < time.time()


def serial_line_status(serialPort):
    # DTE Out Signals, PySerial acts as DTE only
    # This side receive ready
    serialPort.setRTS(1)
    # This side is ready to receive, initiate, or continue a call
    serialPort.setDTR(0)

    # DTE status lines
    # Other side is ready to accept data from the DTE
    print("CTS: ", serialPort.getCTS())
    # Other side is ready to receive and send data
    print("DSR: ", serialPort.getDSR())
    # Other side is receiving a carrier from a remote DCE
    print("CD: ", serialPort.getCD())
    # Other side has detected an incoming ring signal
    print("RI: ", serialPort.getRI())
    print(serialPort)


def save_line(output_filename, line):
    # Append the line to a log file
    output_file = open(output_filename, 'a', newline='')
    output_file.writelines(line)
