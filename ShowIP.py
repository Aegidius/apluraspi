# ShowIP.py

from raspibrick import *

robot = Robot()
display = Display()
ipAddress = robot.getIPAddress("wlan0")
ipAddress = ipAddress.replace(".", "-")
print "IP address:", ipAddress
display.ticker(ipAddress, 5)
