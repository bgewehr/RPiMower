#!/usr/bin/python

import RPi.GPIO as GPIO 
import time

def init():
    # GPIO Mode (BOARD / BCM)
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

    # Setup GPIO variables for left wheel
    global GPIO_leftwheel
    GPIO_leftwheel = 22
    global GPIO_leftwheelDIR
    GPIO_leftwheelDIR = 23
    global GPIO_leftwheelPWM
    GPIO_leftwheelPWM = 27
    global GPIO_leftwheelDC
    GPIO_leftwheelDC = 100

    # Setup GPIO variables for right wheel
    global GPIO_rightwheel
    GPIO_rightwheel = 17
    global GPIO_rightwheelDIR
    GPIO_rightwheelDIR = 18
    global GPIO_rightwheelPWM
    GPIO_rightwheelPWM = 24
    global GPIO_rightwheelDC
    GPIO_rightwheelDC =100

    global PWMFrequency
    PWMFrequency = 1500

    # Initialize GPIO PINS and PWM
    GPIO.setup(GPIO_leftwheel, GPIO.OUT)
    GPIO.setup(GPIO_leftwheelDIR, GPIO.OUT)
    GPIO.setup(GPIO_leftwheelPWM, GPIO.OUT)
    global pwmleft
    pwmleft = GPIO.PWM(GPIO_leftwheelPWM, PWMFrequency)
    pwmleft.start(0)

    GPIO.setup(GPIO_rightwheel, GPIO.OUT)
    GPIO.setup(GPIO_rightwheelDIR, GPIO.OUT)
    GPIO.setup(GPIO_rightwheelPWM, GPIO.OUT)
    global pwmright
    pwmright = GPIO.PWM(GPIO_rightwheelPWM, PWMFrequency)
    pwmright.start(0)

def cleanup():
    GPIO.cleanup()

def forward():
    # forward
    GPIO.output(GPIO_leftwheel, False)
    GPIO.output(GPIO_leftwheelDIR, True)
    GPIO.output(GPIO_rightwheel, False)
    GPIO.output(GPIO_rightwheelDIR, True)
    pwmleft.ChangeDutyCycle(GPIO_leftwheelDC)	
    pwmright.ChangeDutyCycle(GPIO_rightwheelDC)	

def stop():
    # stop
    pwmleft.ChangeDutyCycle(0)
    pwmright.ChangeDutyCycle(0)	
    GPIO.output(GPIO_leftwheel, False)
    GPIO.output(GPIO_leftwheelDIR, False)
    GPIO.output(GPIO_rightwheel, False)
    GPIO.output(GPIO_rightwheelDIR, False)

def backward():
   # backward
    GPIO.output(GPIO_leftwheel, True)
    GPIO.output(GPIO_leftwheelDIR, False)
    GPIO.output(GPIO_rightwheel, True)
    GPIO.output(GPIO_rightwheelDIR, False)
    pwmleft.ChangeDutyCycle(GPIO_leftwheelDC)	
    pwmright.ChangeDutyCycle(GPIO_rightwheelDC)	

def right90():
    # left wheel forward, right wheel stop
    GPIO.output(GPIO_leftwheel, False)
    GPIO.output(GPIO_leftwheelDIR, True)
    GPIO.output(GPIO_rightwheel, False)
    GPIO.output(GPIO_rightwheelDIR, False)
    pwmleft.ChangeDutyCycle(GPIO_leftwheelDC)	
    pwmright.ChangeDutyCycle(GPIO_rightwheelDC)	

def left90():
    # right wheel forward, left whell stop
    GPIO.output(GPIO_leftwheel, False)
    GPIO.output(GPIO_leftwheelDIR, False)
    GPIO.output(GPIO_rightwheel, False)
    GPIO.output(GPIO_rightwheelDIR, True)
    pwmleft.ChangeDutyCycle(GPIO_leftwheelDC)	
    pwmright.ChangeDutyCycle(GPIO_rightwheelDC)	

def right180(leftDC = 0, rightDC = 0):
    # left wheel forward, left wheel backward
    if leftDC == 0:
        leftDC = GPIO_leftwheelDC
    if rightDC == 0:
       rightDC = GPIO_rightwheelDC
    GPIO.output(GPIO_leftwheel, False)
    GPIO.output(GPIO_leftwheelDIR, True)
    GPIO.output(GPIO_rightwheel, True)
    GPIO.output(GPIO_rightwheelDIR, False)
    pwmleft.ChangeDutyCycle(leftDC)
    pwmright.ChangeDutyCycle(rightDC)

def left180(leftDC = 0, rightDC = 0):
    # left wheel backward, right wheel forward
    if leftDC == 0:
        leftDC = GPIO_leftwheelDC
    if rightDC == 0:
       rightDC = GPIO_rightwheelDC
    GPIO.output(GPIO_leftwheel, True)
    GPIO.output(GPIO_leftwheelDIR, False)
    GPIO.output(GPIO_rightwheel, False)
    GPIO.output(GPIO_rightwheelDIR, True)
    pwmleft.ChangeDutyCycle(leftDC)
    pwmright.ChangeDutyCycle(rightDC)

def turn(angle):
    if not angle:
        angle = 1.5
    else:
        angle = angle + 0.15
    stop()
    time.sleep(0.05)
    backward()
    time.sleep(0.75)
    stop()
    time.sleep(0.05)
    if angle < 0:
        left180()
    else:
        right180()
    time.sleep(abs(angle))
    stop()
    time.sleep(0.05)
