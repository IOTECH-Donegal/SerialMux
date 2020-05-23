""""
Main routine for Serial Mux
Forked from the Comm module of SD-Node
Takes two serial inputs and logs them.
Optionally, forward to a UDP address:port

By: JOR
    v0.1    26APR20     First go!
"""
from datetime import datetime
import sys
import socket
import serial
import time
from Classes import Serial, Utilities

output_filename = "logfile.txt"

# Open a UDP server, even through we will not receive
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Hard code the destination port
kplex_IPv4 = "127.0.0.1"
kplex_Port = 2001
print("Expecting to find UDP receiver at " + kplex_IPv4 + ":" + str(kplex_Port))

# Configure the first serial port, this should be the master GPS
Serial_Port1 = serial.Serial(
    port='/dev/ttyACM0',
    baudrate=9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    rtscts=True,
    dsrdtr=True,
    timeout=1
)
Serial_Port1.flushInput()
# Run the receiver thread as a daemon, will be killed automatically on programme exit
serial_port1 = Serial.serialPort(2, "GPS Serial Receiver", Serial_Port1)
try:
    serial_port1.setDaemon(True)
    serial_port1.start()
except:
    print("Error starting first serial thread")
    exit(1)
finally:
    # Wait for threads to start
    time.sleep(1)

# Configure the second serial port
Serial_Port2 = serial.Serial(
    port='/dev/ttyUSB0',
    baudrate=9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    rtscts=True,
    dsrdtr=True,
    timeout=1
)
Serial_Port2.flushInput()
# Run the receiver thread as a daemon, will be killed automatically on programme exit
serial_port2 = Serial.serialPort(3, "Magnetometer Serial Receiver", Serial_Port2)
try:
    serial_port2.setDaemon(True)
    serial_port2.start()
except:
    print("Error starting second serial thread")
    exit(1)
finally:
    # Wait for threads to start
    time.sleep(1)

# Main Loop
try:
    while 1:
        print("press [ctrl][c] at any time to exit...")
        while 1:
            # Receive data from the serial link and relay to UDP server
            if len(serial_port1.read_buffer) > 0:
                try:
                    current_line = str(serial_port1.read_buffer)
                    sock.sendto(bytes(current_line, "utf-8"), (kplex_IPv4, kplex_Port))
                    Utilities.save_line(output_filename, current_line)
                    print('Serial1:' + current_line.strip())
                except Exception as error:
                    print("Main loop error: ", sys.exc_info()[0])
                finally:
                    serial_port1.read_buffer = ""

            # Receive data from the serial link and relay to UDP server
            if len(serial_port2.read_buffer) > 0:
                try:
                    current_line = str(serial_port2.read_buffer)
                    sock.sendto(bytes(current_line, "utf-8"), (kplex_IPv4, kplex_Port))
                    Utilities.save_line(output_filename, current_line)
                    print('Serial2:' + current_line.strip())
                except Exception as error:
                    print("Main loop error: ", sys.exc_info()[0])
                finally:
                    serial_port2.read_buffer = ""

except KeyboardInterrupt:
    print("\n" + "Caught keyboard interrupt, exiting")
finally:
    print("Exiting Main Thread")
    exit(0)
