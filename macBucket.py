#!/usr/bin/python

import time

#import adc
import motorBucket

DEBUG      = True
READ_DELAY = 0.2

# thresholds between non-white and white for each of the sensors
thresholdR = 150
thresholdL = 100


def init ():
    motorBucket.initMotors ()

    initR = 0  # adc.readADC (0)
    initL = 0  # adc.readADC (1)
    return (initR, initL)


def run ((initR, initL)):
    t = time.time ()
    elapsed = 0

    while (elapsed < 3):
        time.sleep (READ_DELAY)

        goForward ()
        elapsed = time.time () - t

        # find the current values of the line sensors
        lineR = 0  # adc.readADC (0)
        lineL = 0  # adc.readADC (1)

        if (DEBUG): print "initR: %d | initL: %d" % (initR, initL)
        if (DEBUG): print "Right: %d |  Left: %d" % (lineR, lineL)

        # make choices and change direction if needed
#        if   (lineR - initR > thresholdR): steerRight ()
#        elif (lineL - initL > thresholdL): steerLeft  ()
#        else:                              goForward  ()
    motorBucket.stopMotors ()


def steerRight ():
    if (DEBUG): print "Steer right!"
    motorBucket.goRight (50)


def steerLeft ():
    if (DEBUG): print "Steer left!"
    motorBucket.goLeft (50)


def goForward ():
    if (DEBUG): print "Go forward."
    motorBucket.goForward (100)


def close ():
    motorBucket.finMotors ()
#    adc.closeADC ()


if __name__ == '__main__':
    try:
        initVals = init ()
        run (initVals)
    except KeyboardInterrupt:
        close ()
