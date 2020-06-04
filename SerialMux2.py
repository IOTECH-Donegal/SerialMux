""""
Main routine for Serial Mux
Forked from the Comm module of SD-Node
Takes two serial inputs and logs them.
Optionally, forward to a UDP address:port

By: JOR
    v0.1    26APR20     First go!
    v0.2    24MAY20     Removed all complexity, threading, etc.
"""
from datetime import datetime
import sys
import socket
import serial

# Create the log file and open it
output_filename = "logfile.txt"
output_file = open(output_filename, 'a', newline='')

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
    timeout=.1
)
Serial_Port1.flushInput()

# Configure the second serial port
Serial_Port2 = serial.Serial(
    port='/dev/ttyUSB0',
    baudrate=9600,
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
    while 1:
        # Receive data from the serial link and relay to UDP server
        read_buffer1 = Serial_Port1.readline().decode('ascii', errors='replace')
        while len(read_buffer1) != 0:
            try:
                current_line = str(read_buffer1)
                sock.sendto(bytes(current_line, "utf-8"), (kplex_IPv4, kplex_Port))
                output_file.writelines(current_line)
                print('GPS:' + current_line.strip())
            except Exception as error:
                print("Main loop error: ", sys.exc_info()[0])
            finally:
                read_buffer1 = Serial_Port1.readline().decode('ascii', errors='replace')

        # Receive data from the serial link and relay to UDP server
        read_buffer2 = Serial_Port2.readline().decode('ascii', errors='replace')
        while len(read_buffer2) != 0:
            try:
                current_line = str(read_buffer2)
                sock.sendto(bytes(current_line, "utf-8"), (kplex_IPv4, kplex_Port))
                output_file.writelines(current_line)
                print('Magnetometer:' + current_line.strip())
            except Exception as error:
                print("Main loop error: ", sys.exc_info()[0])
            finally:
                read_buffer2 = Serial_Port2.readline().decode('ascii', errors='replace')

except KeyboardInterrupt:
    print("\n" + "Caught keyboard interrupt, exiting")
finally:
    print("Exiting Main Thread")
    exit(0)