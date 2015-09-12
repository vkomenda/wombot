#!/usr/bin/python
import time
import math
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
DEBUG = 1

def readQD(pinQD):
    GPIO.setup(pinQD, GPIO.OUT)
    GPIO.output(pinQD, True)
    time.sleep(0.00001)      # 10 microseconds

    GPIO.setup(pinQD, GPIO.IN)  
    t = time.time()
    elapsed = 0

    while (GPIO.input(pinQD) & (elapsed < 0.003)):
        elapsed = time.time() - t
                             # miliseconds: less means lighter and
                             # more light is reflected

    percent = 100 - math.trunc (math.floor (elapsed * 100000 / 3))
    return max (0, min (100, percent))

if __name__ == "__main__":
    PIN_LEFT  = 24
    PIN_RIGHT = 25

    while True:
        leftQD  = readQD(PIN_LEFT)
        rightQD = readQD(PIN_RIGHT)

        if DEBUG:
            print "leftQD",  leftQD
            print "rightQD", rightQD

        time.sleep(1.0)
