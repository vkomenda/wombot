from time import sleep
import sys

import irsensor

DEBUG = True


class IR2:

    def __init__ (self, left, right):
        self.pinLeft  = left
        self.pinRight = right
        if DEBUG:
            print "Initialising the infra-red sensor pair."

    def __del__ (self):
        if DEBUG:
            print "Finalising the infra-red sensor pair."

    def read (self):
        readingRight = irsensor.readQD (self.pinRight)
        readingLeft  = irsensor.readQD (self.pinLeft)
        return (readingLeft, readingRight)
