#!/bin/bash
# by: JOR
# Date: 06JUN20
# Function: Run serial logging script
# Leave this script in /home/pi
# Script: SerialMux.sh

HOMEPATH="/home/pi"

echo "Starting to log"
sudo python3 $HOMEPATH/SerialMux2.py 2>$HOMEPATH/SerialMux2.err


