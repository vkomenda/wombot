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
        adc = [0,0,0,0,0,0,0,0]
        while True:

            for i in range (7):
                adc[i] = readADC (i)

            print "Analogue-to-digital values: ", adc

            time.sleep (0.2)

    except KeyboardInterrupt:
        closeADC ()
