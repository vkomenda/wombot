#!/usr/bin/python

import RPi.GPIO as GPIO

LED  = 17

GPIO.setmode (GPIO.BCM)
GPIO.setup (LED, GPIO.OUT)

def tick (ticks, mode):
    ticks = ticks + 1

    if (mode == 0):
        GPIO.output (LED, False)
    if (mode == 1):
        t = ticks % 10
        if (t == 0):
            GPIO.output (LED, False)
        elif (t == 3):
            GPIO.output (LED, True)
    elif (mode == 2):
        t = ticks % 12
        if (t == 0 or t == 4):
            GPIO.output (LED, False)
        elif (t == 2 or t == 6):
            GPIO.output (LED, True)
    elif (mode == 3):
        t = ticks % 20
        if (t == 0 or t == 4 or t == 8):
            GPIO.output (LED, False)
        elif (t == 2 or t == 6 or t == 10):
            GPIO.output (LED, True)
