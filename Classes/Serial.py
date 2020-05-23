import threading
import sys
import serial

"""
    AsciiSerialPort
    By: JOR
    v0.1 12APR14    Initial test, uses separate classes for send and receive
    v0.2 13APR14    Single class, threading within the class, line oriented
    v0.3 10JUL18    Recoded for Python 3.x
"""


class serialPort(threading.Thread):
    def __init__(self, thread_id, name, serial_port):
        threading.Thread.__init__(self)
        self.name = name
        self.thread_id = thread_id
        """ Set the serial port to whatever was specified when the class was called """
        self.serial_port = serial_port
        """ Create a buffer for input data """
        self.read_buffer = []
        self.write_buffer = []
        self.message = ""

    def run(self):
        print("Starting thread " + str(self.thread_id) + " - " + self.name + "\n")
        self.serial_port.rts = True
        while 1:
            try:
                self.read_buffer = self.serial_port.readline().decode('ascii', errors='replace')
            except serial.SerialException as error:
                print("Serial - Error reading data: %s", error)
            except TypeError as error:
                print("Serial - Type error receiving serial data:", sys.exc_info()[0])
            except Exception as error:
                print("Serial - Unexpected error receiving serial data:", sys.exc_info()[0])
