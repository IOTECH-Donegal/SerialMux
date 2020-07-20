""""
Main routine for Serial Mux
Forked from the Comm module of SD-Node
Takes two serial inputs and logs them.
Optionally, forward to a UDP address:port
Tested with Python >=3.6
By: JOR
    v0.1    26APR20     First go!
    v0.2    24MAY20     Removed all complexity, threading, etc.
    v0.3    06JUN20	    Modified as a single serial logger
"""

from datetime import datetime
import sys
import socket
import serial

# Create the log file and open it
output_filename = "/home/pi/survey.log"
output_file = open(output_filename, 'a', newline='')

# Open a UDP server, even through we will not receive
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Hard code the destination port, expect KPlex, but can be anything
kplex_IPv4 = "127.0.0.1"
kplex_Port = 2001
print("Expecting to find UDP receiver at " + kplex_IPv4 + ":" + str(kplex_Port))

# Configure the first serial port, this should be the master GPS
# U-Blox connected directly should be ttyACM0
Serial_Port1 = serial.Serial(
    # port='COM10',
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

# Configure the second serial port
# A RS232-USB dongle should be ttyUSBx
# A Zihatec RS422 converter is ttyS0 and 4800
Serial_Port2 = serial.Serial(
    # port='COM11',
    port='/dev/ttyS0',
    baudrate=4800,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    rtscts=True,
    dsrdtr=True,
    timeout=.1
)
Serial_Port2.flushInput()

# Main Loop
try:
    print("press [ctrl][c] at any time to exit...")
    while True:
        # Receive data from serial link 1
        read_buffer1 = Serial_Port1.readline().decode('ascii', errors='replace')
        while len(read_buffer1) != 0:
            try:
                current_line = str(read_buffer1)
                # Send to UDP server
                sock.sendto(bytes(current_line, "utf-8"), (kplex_IPv4, kplex_Port))
                # Log the data
                output_file.writelines(current_line)
                print('GPS:' + current_line.strip())
            except Exception as error:
                print("Main loop error: ", sys.exc_info()[0])
            finally:
                read_buffer1 = Serial_Port1.readline().decode('ascii', errors='replace')

        # Receive data from serial link 2
        read_buffer2 = Serial_Port2.readline().decode('ascii', errors='replace')
        while len(read_buffer2) != 0:
            try:
                current_line = str(read_buffer2)
                # Send to UDP server
                sock.sendto(bytes(current_line, "utf-8"), (kplex_IPv4, kplex_Port))
                # Log the data
                output_file.writelines(current_line)
                print('Magnetometer:' + current_line.strip())
            except Exception as error:
                print("Main loop error: ", sys.exc_info()[0])
            finally:
                read_buffer2 = Serial_Port2.readline().decode('ascii', errors='replace')

except KeyboardInterrupt:
    print("\n" + "Caught keyboard interrupt, exiting")
    exit(0)
finally:
    print("Exiting Main Thread")
    exit(0)
