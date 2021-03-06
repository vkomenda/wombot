#!/usr/bin/python

from time  import sleep

import adc
import motor
import led
import os

DEBUG      = True
READ_DELAY = 0.2

ADC_LINE_LEFT    = 0
ADC_LINE_RIGHT   = 3
ADC_BUTTON       = 4
ADC_SWITCH_RIGHT = 5
ADC_SWITCH_LEFT  = 6

# thresholds between non-white and white for each of the sensors
thresholdR = 15
thresholdL = 15
#thresholdR = 70
#thresholdL = 70

# modes
MODE_INIT = 0
MODE_WAIT = 1
MODE_LINE = 2
MODE_MAZE = 3

DIR_FWD   = 0
DIR_LEFT  = 1
DIR_RIGHT = 2

SENSE_NONE  = 0
SENSE_LEFT  = 1
SENSE_RIGHT = 2
SENSE_BOTH  = 3

def init ():
    motor.initMotors ()

    initR = adc.readADC (ADC_LINE_RIGHT)
    initL = adc.readADC (ADC_LINE_LEFT)
    return (initR, initL)

def showMode (mode):
    if   (mode == MODE_INIT): return "INIT"
    elif (mode == MODE_WAIT): return "WAIT"
    elif (mode == MODE_LINE): return "LINE"
    elif (mode == MODE_MAZE): return "MAZE"
    else:                     return "NONE"

def lineFollowerTransition ((direc, sense)):
    if   (sense == SENSE_NONE):
        if   (direc == DIR_FWD):   return DIR_FWD
        elif (direc == DIR_LEFT):  return DIR_FWD
        elif (direc == DIR_RIGHT): return DIR_FWD
        else:                      return DIR_FWD
    elif (sense == SENSE_LEFT):
        if   (direc == DIR_FWD):   return DIR_LEFT
        elif (direc == DIR_LEFT):  return DIR_LEFT
        elif (direc == DIR_RIGHT): return DIR_LEFT
        else:                      return DIR_FWD
    elif (sense == SENSE_RIGHT):
        if   (direc == DIR_FWD):   return DIR_RIGHT
        elif (direc == DIR_LEFT):  return DIR_RIGHT
        elif (direc == DIR_RIGHT): return DIR_RIGHT
        else:                      return DIR_FWD
    elif (sense == SENSE_BOTH):
        if   (direc == DIR_FWD):   return DIR_LEFT
        elif (direc == DIR_LEFT):  return DIR_RIGHT
        elif (direc == DIR_RIGHT): return DIR_LEFT
        else:                      return DIR_FWD

def mazeSolverTransition ((direc, sense)):
    if   (sense == SENSE_NONE):
        if   (direc == DIR_FWD):   return DIR_LEFT
        elif (direc == DIR_LEFT):  return DIR_LEFT
        elif (direc == DIR_RIGHT): return DIR_LEFT
        else:                      return DIR_FWD
    elif (sense == SENSE_LEFT):
        if   (direc == DIR_FWD):   return DIR_FWD
        elif (direc == DIR_LEFT):  return DIR_FWD
        elif (direc == DIR_RIGHT): return DIR_FWD
        else:                      return DIR_FWD
    elif (sense == SENSE_RIGHT):
        if   (direc == DIR_FWD):   return DIR_RIGHT
        elif (direc == DIR_LEFT):  return DIR_RIGHT
        elif (direc == DIR_RIGHT): return DIR_LEFT
        else:                      return DIR_FWD
    elif (sense == SENSE_BOTH):
        if   (direc == DIR_FWD):   return DIR_RIGHT
        elif (direc == DIR_LEFT):  return DIR_RIGHT
        elif (direc == DIR_RIGHT): return DIR_RIGHT
        else:                      return DIR_FWD

def run ((initR, initL)):
    mode = MODE_INIT
    reset = False
    resetR = initR
    resetL = initL
    ticks = 0
    sense = SENSE_NONE
    direc = DIR_FWD

    while True:
        led.tick (ticks, mode)
        ticks = ticks + 1

        sleep (READ_DELAY)

        # find the current values of the line sensors
        lineR   = adc.readADC (ADC_LINE_RIGHT)
        lineL   = adc.readADC (ADC_LINE_LEFT)
        button  = adc.readADC (ADC_BUTTON)
        switchR = adc.readADC (ADC_SWITCH_RIGHT)
        switchL = adc.readADC (ADC_SWITCH_LEFT)

        if (adc.high (button) == True):
            reset = True

        if (adc.high (switchR) == True and mode != MODE_LINE):
            mode = MODE_LINE
            reset = True
        elif (adc.high (switchL) == True and mode != MODE_MAZE):
            mode = MODE_MAZE
            reset = True
        elif (adc.low (switchR) == True and adc.low (switchL) == True and
              mode != MODE_WAIT):
            mode = MODE_WAIT
            motor.stopMotors ()

        if (reset == True):
            ticks = 0
            led.tick (ticks, mode)

            if (mode == MODE_LINE or mode == MODE_MAZE):
                motor.stopMotors ()
                sleep (5)

                resetR = adc.readADC (ADC_LINE_RIGHT)
                resetL = adc.readADC (ADC_LINE_LEFT)

            elif (mode == MODE_WAIT):
                os.system ("sudo shutdown -h now")

        if (DEBUG):
            print "resetR: %d | resetL: %d" % (resetR, resetL)
            print "Right: %d |  Left: %d" % (lineR, lineL)
            print "Mode: %s | Reset: %s" % (showMode (mode), reset)
            print "Button, switch R, switch L: %d, %d, %d" % (adc.high (button), adc.high (switchR), adc.high (switchL))

        if (mode == MODE_WAIT and reset == True):
            motor.stopMotors ()

        if (reset == False):
            sense = SENSE_NONE
            if (lineR - resetR > thresholdR): sense |= SENSE_RIGHT
            if (lineL - resetL > thresholdL): sense |= SENSE_LEFT

            if   (mode == MODE_LINE):
                direc = lineFollowerTransition((direc, sense))
                if   (direc == DIR_RIGHT): steerRight ()
                elif (direc == DIR_LEFT):  steerLeft  ()
                else:                      goForward  ()

            elif (mode == MODE_MAZE):
                direc = mazeSolverTransition((direc, sense))
                if   (direc == DIR_RIGHT): giveInRight ()
                elif (direc == DIR_LEFT):  swayLeft    ()
                else:                      goForward   ()

        reset = False


def steerRight ():
    if (DEBUG): print "Steer right!"
    motor.goRight (80)


def steerLeft ():
    if (DEBUG): print "Steer left!"
    motor.goLeft (80)


def goForward ():
    if (DEBUG): print "Go forward."
    motor.goForward (80)

def swayLeft ():
    if (DEBUG): print "Sway left."
    motor.rf.ChangeDutyCycle (70)
    motor.rb.ChangeDutyCycle (0)
    motor.lf.ChangeDutyCycle (40)
    motor.lb.ChangeDutyCycle (0)

def giveInRight ():
    if (DEBUG): print "Give in right."
    motor.rf.ChangeDutyCycle (0)
    motor.rb.ChangeDutyCycle (70)
    motor.lf.ChangeDutyCycle (0)
    motor.lb.ChangeDutyCycle (0)

def close ():
    motor.finMotors ()
    adc.closeADC ()


if __name__ == '__main__':
    try:
        initVals = init ()
        run (initVals)
    except KeyboardInterrupt:
        close ()
