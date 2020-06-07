#!/bin/bash
# by: JOR
# Date: 06JUN20
# Function: autoexec.bat for Linux
# Leave this script in /home/pi
# Script: jor.sh

HOMEPATH="/home/pi"

echo "Backing up existing log file"
DIRECTORYNAME=`date '+%Y%m%d'`
FILENAME=`date '+%H%M'`

echo "Creating directory "$DIRECTORYNAME
echo "Saving configuration as "$FILENAME

mkdir $HOMEPATH/$DIRECTORYNAME
cp $HOMEPATH/survey.log $HOMEPATH/$DIRECTORYNAME/$HOSTNAME-$FILENAME
cat /dev/null > $HOMEPATH/survey.log

echo "Setting time from GPS"
sleep 20
sudo python3 $HOMEPATH/SetUTC.py 2>$HOMEPATH/SetUTC.err

