""""
Main routine to time sync a Linux server which is not network connected.
Assume Serial1 is a GPS
Tested with Python >=3.6 on RPi running OpenPlotter 2.0
By: JOR
    v0.1    06JUN20     First go!

"""

import os
import serial

print('This utility run at startup to set time and date on RPi')
print('Accuracy no better than 1 second')

try:

    # Configure the first serial port, this should be the master GPS
    Serial_Port1 = serial.Serial(
        # port='COM10',
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

    while True:
        read_buffer1 = Serial_Port1.readline().decode('ascii', errors='replace')
        nmea_full_sentence = str(read_buffer1)

        # Break it up into fields
        list_of_values = nmea_full_sentence.split(',')
        # Process the talker ID and assign it to a property
        if list_of_values[0] == '$GNZDA':
            # Get time in the form 114645.00
            utctime = list_of_values[1]
            utchour = utctime[0:2]
            utcmin = utctime[2:4]
            utcsec = utctime[4:6]
            day = list_of_values[2]
            month = list_of_values[3]
            year = list_of_values[4]
            # sudo date --set '2017-12-31 20:45:00'
            system_date = year + '-' + month + '-' + day
            system_time = utchour + ':' + utcmin + ':' + utcsec
            time_string = system_date + " " + system_time
            os.system('sudo date -u --set "%s" ' % time_string)
            break

except serial.SerialException:
    print('Error opening serial port...is the GPS connected?')
    exit(0)
