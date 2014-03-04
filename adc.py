#!/usr/bin/python

import time
import spidev

spi = spidev.SpiDev ()
spi.open (0,0)

def readADC (adcnum):
    if (adcnum < 0 | adcnum > 7): return -1

    r = spi.xfer2 ([1, (8 + adcnum) << 4, 0])
    adcout = ((r[1] & 3) << 8) + r[2]

    return adcout


def closeADC ():
    spi.close ()


if __name__ == "__main__":
    try:
        while True:

            adc0 = readADC (0)
            print "ADC 0: ", adc0

            adc1 = readADC (1)
            print "ADC 1: ", adc1

#            adc2 = readADC (2)
#            print "ADC 2: ", adc2

            time.sleep (0.2)

    except KeyboardInterrupt:
        closeADC ()
