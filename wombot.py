#!/usr/bin/python

from time  import sleep

import adc
import motor

DEBUG      = True
READ_DELAY = 0.2

# thresholds between non-white and white for each of the sensors
thresholdR = 150
thresholdL = 100


def init ():
    motor.initMotors ()

    initR = adc.readADC (0)
    initL = adc.readADC (1)
    return (initR, initL)


def run ((initR, initL)):
    while True:
        sleep (READ_DELAY)

        # find the current values of the line sensors
        lineR = adc.readADC (0)
        lineL = adc.readADC (1)

        if (DEBUG): print "initR: %d | initL: %d" % (initR, initL)
        if (DEBUG): print "Right: %d |  Left: %d" % (lineR, lineL)

        # make choices and change direction if needed
        if   (lineR - initR > thresholdR): steerRight ()
        elif (lineL - initL > thresholdL): steerLeft  ()
        else:                              goForward  ()


def steerRight ():
    if (DEBUG): print "Steer right!"
    motor.goRight (50)


def steerLeft ():
    if (DEBUG): print "Steer left!"
    motor.goLeft (50)


def goForward ():
    if (DEBUG): print "Go forward."
    motor.goForward (40)


def close ():
    motor.finMotors ()
    adc.closeADC ()


if __name__ == '__main__':
    try:
        initVals = init ()
        run (initVals)
    except KeyboardInterrupt:
        close ()
