#!/usr/bin/python

import RPi.GPIO as GPIO
from time import sleep

RIGHT_FWD  = 4
RIGHT_BACK = 18
LEFT_FWD   = 24
LEFT_BACK  = 23

GPIO.setmode (GPIO.BCM)

GPIO.setup (RIGHT_FWD,  GPIO.OUT)
GPIO.setup (RIGHT_BACK, GPIO.OUT)
GPIO.setup (LEFT_FWD,   GPIO.OUT)
GPIO.setup (LEFT_BACK,  GPIO.OUT)

rf = GPIO.PWM (RIGHT_FWD,  50)
rb = GPIO.PWM (RIGHT_BACK, 50)
lf = GPIO.PWM (LEFT_FWD,   50)
lb = GPIO.PWM (LEFT_BACK,  50)

def initMotors ():
    rf.start (0)
    rb.start (0)
    lf.start (0)
    lb.start (0)

def stopMotors ():
    rf.ChangeDutyCycle (0)
    rb.ChangeDutyCycle (0)
    lf.ChangeDutyCycle (0)
    lb.ChangeDutyCycle (0)

# speed ranges over [0..100]
def goForward (speed):
    rf.ChangeDutyCycle (speed)
    rb.ChangeDutyCycle (0)
    lf.ChangeDutyCycle (speed)
    lb.ChangeDutyCycle (0)

def goBack (speed):
    rf.ChangeDutyCycle (0)
    rb.ChangeDutyCycle (speed)
    lf.ChangeDutyCycle (0)
    lb.ChangeDutyCycle (speed)

def goRight (speed):
    rf.ChangeDutyCycle (0)
    rb.ChangeDutyCycle (0)
    lf.ChangeDutyCycle (speed)
    lb.ChangeDutyCycle (0)

def goLeft (speed):
    rf.ChangeDutyCycle (speed)
    rb.ChangeDutyCycle (0)
    lf.ChangeDutyCycle (0)
    lb.ChangeDutyCycle (0)

def finMotors ():
    rf.stop ()
    rb.stop ()
    lf.stop ()
    lb.stop ()
    GPIO.cleanup ()
