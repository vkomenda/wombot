#!/usr/bin/env python

from array import array
from time  import sleep
import threading
import socket
import sys
import struct

import adc


DEBUG = True


DEFAULT_HOST   = '127.0.0.1'
PORT           = 42001
SOCKET_TIMEOUT = 1
SENDER_DELAY   = 0.5  # in seconds


SCRATCH_NAME_INPUT = (
    "infrared-right",
    "infrared-left",
    "adc2",
    "adc3",
    "adc4",
    "adc5",
    "adc6",
    "adc7")


class ScratchSender (threading.Thread):
    def __init__ (self, sock):
        threading.Thread.__init__ (self)
        self.scratchSock = sock
        self._stop = threading.Event ()
        # self.ir2 = irpair.IR2 (24, 25)

    def stop (self):
        self._stop.set ()

    def stopped (self):
        return self._stop.isSet ()

    def run (self):
        adcTolerance = 5
        adcPins = 3
        adcLast = [0,0,0,0,0,0,0,0]
        adcOut  = [0,0,0,0,0,0,0,0]
        adcChanged = [False,False,False,False,False,False,False,False]

        while not self.stopped ():
            sleep (SENDER_DELAY)

            for i in range (adcPins):
                adcChanged[i] = False

            updates = []
            for i in range (adcPins):
                adcOut[i] = adc.readADC (i)
                if (abs (adcOut[i] - adcLast[i]) > adcTolerance):
                    adcChanged[i] = True
                    updates.append ((SCRATCH_NAME_INPUT[i], adcOut[i]))

            if (DEBUG): print "ADC values: " , adcOut

            if updates != []:
                try:
                    self.sendUpdates (updates)
                    for i in range (adcPins):
                        if (changed[i]): adcLast = adcOut
                except Exception as e:
                    print e
                    break

    def sendUpdates (self, updates):
        for upd in updates:
            cmd = 'sensor-update "%s" %d' % upd
            if DEBUG: print "Sending: %s" % cmd
            self.sendScratchCommand (cmd)

    def sendScratchCommand(self, cmd):
        n = len (cmd)
        a = array ('c')
        a.append (chr((n >> 24) & 0xFF))
        a.append (chr((n >> 16) & 0xFF))
        a.append (chr((n >>  8) & 0xFF))
        a.append (chr( n        & 0xFF))
        self.scratchSock.send (a.tostring () + cmd)


class ScratchListener (threading.Thread):
    def __init__ (self, sock):
        threading.Thread.__init__ (self)
        self.scratchSock = sock
        self._stop = threading.Event ()

    def stop (self):
        self._stop.set ()

    def stopped (self):
        return self._stop.isSet ()

    def run (self):
        while not self.stopped ():
            try:
                data = self.scratchSock.recv(BUFFER_SIZE)
                print "Received from Scratch: %s", data
            except socket.timeout:
                continue
            except:
                break


def createSocket (host, port):
    try:
        scratchSock = socket.socket (socket.AF_INET, socket.SOCK_STREAM)
        scratchSock.connect ((host, port))
    except socket.error:
        print "There was an error connecting to Scratch!"
        print "I couldn't find a Mesh session at host: %s, port: %s" % (host, port)
        sys.exit (1)

    return scratchSock


def initialise ():
    return 0


def finalise ():
    return 0


def cleanupThreads (threads):
    for thread in threads:
        thread.stop ()

    for thread in threads:
        thread.join ()


if __name__ == '__main__':
    if len (sys.argv) > 1:
        host = sys.argv[1]
    else:
        host = DEFAULT_HOST

    # open the socket
    print 'Connecting...' ,
    sock = createSocket (host, PORT)
    print 'Connected!'

    sock.settimeout (SOCKET_TIMEOUT)

    initialise ()

    listener = ScratchListener (sock)
    sender   = ScratchSender   (sock)
    listener . start ()
    sender   . start ()

    # exit by pressing Ctrl-c in the console
    try:
        while True:
            pass
    except:
        cleanupThreads ((listener, sender))
        finalise ()
        sys.exit()
