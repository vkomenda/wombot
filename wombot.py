#!/usr/bin/env python

from array import array
from time  import sleep
import sys
import struct

import adc
import motor

DEBUG = True
READ_DELAY = 0.2

def run ():
    adcTolerance = 5
    adcPins = 3
    adcLast = [0,0,0,0,0,0,0,0]
    adcIn  = [0,0,0,0,0,0,0,0]
    adcChanged = [False,False,False,False,False,False,False,False]

    while True:
        sleep (READ_DELAY)

        for i in range (adcPins):
            adcChanged[i] = False

        updates = []
        for i in range (adcPins):
            adcIn[i] = adc.readADC (i)
            if (abs (adcIn[i] - adcLast[i]) > adcTolerance):
                adcChanged[i] = True

        if (DEBUG): print "Analogue-to-digital ports: " , adcIn

        for i in range (adcPins):
            if (adcChanged[i]): adcLast = adcIn


if __name__ == '__main__':
    run ()
