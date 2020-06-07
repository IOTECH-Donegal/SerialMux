# 23MAY20: JOR
## SerialMux
- Created this as a Kplex replacement.
- Working, tested on Raspbian Buster, vanilla.
- This version setup to take a GPS on one serial port and the Magnetometer on the other.

## SerialMux2
- Cut down and simplified!
- Stable, use this version only!!
- This version takes up to 2 serial inputs, logs them, sends them to a UDP_IP:Port

## SerialMuxGUI
- Works on Windows, hangs on Ubuntu, not ready for use!

## SetUTC
The problem with a PI is no RTC, and OpenCPN doesn't time sync!
Solution is create an autoexec.bat file for linux
This also sorts out directories and backups at startup

- Copy SetUTC.py to /home/pi
- Copy jor.sh to /home/pi 
- edit /etc/rc.local and add
  sudo /home/pi/jor.sh

## Run console on GUI screen





