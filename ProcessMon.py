# ProcessMonitor.py

import subprocess, os
from threading import Thread
from raspibrick import *

def onButtonEvent(event):
    global isInterrupted
    if event == BUTTON_PRESSED:
        print "Button pressed"
        isInterrupted = True

# ------------------------- main ------------------------------------
print "ProcessMonitor starting"
robot = Robot()
led = Led(LED_LEFT)
led.setColor(0, 10, 0)
Tools.delay(10000)  # Wait until raspi is up
led.setColor(0, 0, 10)
robot.addButtonListener(onButtonEvent)
display = Display()
isInterrupted = False
count = 0
ipAddress = robot.getIPAddress("wlan0")
if ipAddress == "0.0.0.0":
    display.setText("AP--")
    print "Trying to get IP address"
    while not isInterrupted and count < 40:  # Try 20 s to get IP address
        ipAddress = robot.getIPAddress("wlan0")
        if ipAddress != "0.0.0.0":
            break
        count += 1
        Tools.delay(500)
    display.clear()
if ipAddress == "0.0.0.0":
    print "No IP found"
Tools.delay(2000)
if not isInterrupted:
    ipAddress = ipAddress.replace(".", "-")
    print "IP address:", ipAddress
    display.ticker(ipAddress, 2)
    while not isInterrupted and display.isTickerAlive():
        Tools.delay(100)
display.stopTicker()
print "Initialization done."
#Tools.delay(3000)

isRunning = True
while isRunning:
    print "Spawning IdleProc..."
    # Blocking call
    rc = subprocess.call(["/usr/bin/python", "/home/pi/brickgate/IdleProcess.py"])
    print "Returning from IdleProc with exit code:", rc
    if rc == 1:
        print "Spawning user app MyApp.py..."
        rc = subprocess.call(["/usr/bin/python", "/home/pi/scripts/MyApp.py"])
        print "Returning from MyApp with exit code:", rc
    elif rc == 2:
        print "Spawning BrickGate server..."
        rc = subprocess.call(["/usr/bin/python", "/home/pi/brickgate/BrickGate.py"])
        print "Returning from BrickGate with exit code:", rc
    elif rc == 3:
        print "Shutting down now..."
        isRunning = False
print "Shutdown process starting..."
display.setText("8YE ", [1, 0, 0])
Tools.delay(3000)
display.clear()
led.setColor(20, 0, 0)
Tools.delay(2000)
os.system("sudo shutdown -h now")





