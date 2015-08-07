# IdleProcess.py

import sys
from threading import Thread

from raspibrick import *


def onButtonEvent(event):
    global rc, isAlive, shutdown, isShutdownPending, isShutdownCanceled
    if not isAlive:
        return
    if event == BUTTON_PRESSED:
        print "Button pressed"
        if isShutdownPending:
            if ir_center.getValue() == 1:
               shutdown = True
               rc = 3
               isAlive = False
            else:
                isShutdownPending = False
                led.setColor(0, 0, 100)
                display.setText("1dLE")
                isShutdownCanceled = True
    elif event == BUTTON_LONGPRESSED:
        print "Button long pressed"
        if ir_center.getValue() == 1:
            if not isShutdownPending:
                isShutdownPending = True
                isShutdownCanceled = False
                display.setText("oooo")
                led.setColor(100, 0, 0)
        else:
            isShutdownPending = False
            rc = 2
            isAlive = False
    elif event == BUTTON_RELEASED:
        if isShutdownPending or isShutdownCanceled:
            isShutdownCanceled = False
            return
        print "Button released"
        rc = 1
        isAlive = False


print "IdleProcess starting"
rc = 0
robot = Robot()
robot.addButtonListener(onButtonEvent)
led = Led(LED_LEFT)
led.setColor(0, 0, 100) # Announce, we are running
display = Display()
display.setText("1dLE")
ir_center = InfraredSensor(IR_CENTER)
isAlive = True
isShutdownPending = False
isShutdownCanceled = False
while isAlive:
    Tools.delay(1000)
display.clear()
led.setColor(0, 0, 0)
Tools.delay(1000)
print "Returning to parent process with rc:", rc
sys.exit(rc)



