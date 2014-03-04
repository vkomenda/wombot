#!/usr/bin/env python

import RPi.GPIO as GPIO
from time import sleep

RIGHT_FWD  = 17
RIGHT_BACK = 22
LEFT_FWD   = 23
LEFT_BACK  = 18

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

def goForward ():
    rf.ChangeDutyCycle (40)
    rb.ChangeDutyCycle (0)
    lf.ChangeDutyCycle (40)
    lb.ChangeDutyCycle (0)

def goBack ():
    rf.ChangeDutyCycle (0)
    rb.ChangeDutyCycle (40)
    lf.ChangeDutyCycle (0)
    lb.ChangeDutyCycle (40)

def goRight ():
    rf.ChangeDutyCycle (20)
    rb.ChangeDutyCycle (0)
    lf.ChangeDutyCycle (0)
    lb.ChangeDutyCycle (0)

def goLeft ():
    rf.ChangeDutyCycle (0)
    rb.ChangeDutyCycle (0)
    lf.ChangeDutyCycle (20)
    lb.ChangeDutyCycle (0)

def stopMotors ():
    rf.stop ()
    rb.stop ()
    lf.stop ()
    lb.stop ()
    GPIO.cleanup ()
