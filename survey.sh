#!/bin/bash
# by: JOR
# Date: 07JUN20
# Function: autoexec.bat for Linux
# Leave this script in /home/pi
# Script: survey.sh

HOMEPATH="/home/survey"

echo "Backing up existing log file"
DIRECTORYNAME=`date '+%Y%m%d'`
FILENAME=`date '+%H%M'`

echo "Creating directory "$DIRECTORYNAME
echo "Saving configuration as "$FILENAME

mkdir $HOMEPATH/$DIRECTORYNAME
cp $HOMEPATH/survey.log $HOMEPATH/$DIRECTORYNAME/$HOSTNAME-$FILENAME
cat /dev/null > $HOMEPATH/survey.log

echo "Setting time from GPS"
sleep 5
sudo python3 $HOMEPATH/SetUTC.py 2>$HOMEPATH/SetUTC.err

echo "Starting to log"
sudo python3 $HOMEPATH/SerialMux2.py 2>$HOMEPATH/SerialMux2.err




