import RPi.GPIO as GPIO
import time

def init():
    # GPIO Mode (BOARD / BCM)
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    # Setup GPIO
    global GPIO_leftwheel
    GPIO_leftwheel = 17
    global GPIO_leftwheelDIR
    GPIO_leftwheelDIR = 18
    global GPIO_leftwheelPWM
    GPIO_leftwheelPWM = 24
    global GPIO_leftwheelDC
    GPIO_leftwheelDC = 100

    global GPIO_rightwheel
    GPIO_rightwheel = 22
    global GPIO_rightwheelDIR
    GPIO_rightwheelDIR = 23
    global GPIO_rightwheelPWM
    GPIO_rightwheelPWM = 27
    global GPIO_rightwheelDC
    GPIO_rightwheelDC = 95

    global PWMFrequency
    PWMFrequency = 50

    GPIO.setup(GPIO_leftwheel, GPIO.OUT)
    GPIO.setup(GPIO_leftwheelDIR, GPIO.OUT)
    GPIO.setup(GPIO_leftwheelPWM, GPIO.OUT)
    global pwmleft
    pwmleft = GPIO.PWM(GPIO_leftwheelPWM, PWMFrequency)

    GPIO.setup(GPIO_rightwheel, GPIO.OUT)
    GPIO.setup(GPIO_rightwheelDIR, GPIO.OUT)
    GPIO.setup(GPIO_rightwheelPWM, GPIO.OUT)
    global pwmright
    pwmright = GPIO.PWM(GPIO_rightwheelPWM, PWMFrequency)

def cleanup():
    GPIO.cleanup()

def forward():
    # forward
    GPIO.output(GPIO_leftwheel, True)
    GPIO.output(GPIO_leftwheelDIR, False)
    GPIO.output(GPIO_rightwheel, True)
    GPIO.output(GPIO_rightwheelDIR, False)
    pwmleft.start(GPIO_leftwheelDC)	
    pwmright.start(GPIO_rightwheelDC)	

def stop():
    # stop
    pwmleft.stop()
    pwmright.stop()	
    GPIO.output(GPIO_leftwheel, False)
    GPIO.output(GPIO_leftwheelDIR, False)
    GPIO.output(GPIO_rightwheel, False)
    GPIO.output(GPIO_rightwheelDIR, False)

def backward():
   # backward
    GPIO.output(GPIO_leftwheel, False)
    GPIO.output(GPIO_leftwheelDIR, True)
    GPIO.output(GPIO_rightwheel, False)
    GPIO.output(GPIO_rightwheelDIR, True)
    pwmleft.start(GPIO_leftwheelDC)	
    pwmright.start(GPIO_rightwheelDC)	

def right90():
    # left wheel forward, right wheel stop
    GPIO.output(GPIO_leftwheel, True)
    GPIO.output(GPIO_leftwheelDIR, False)
    GPIO.output(GPIO_rightwheel, False)
    GPIO.output(GPIO_rightwheelDIR, False)
    pwmleft.start(GPIO_leftwheelDC)	
    pwmright.start(GPIO_rightwheelDC)	

def left90():
    # right wheel forward, left whell stop
    GPIO.output(GPIO_leftwheel, False)
    GPIO.output(GPIO_leftwheelDIR, False)
    GPIO.output(GPIO_rightwheel, True)
    GPIO.output(GPIO_rightwheelDIR, False)
    pwmleft.start(GPIO_leftwheelDC)	
    pwmright.start(GPIO_rightwheelDC)	

def right180():
    # left wheel forward, left wheel backward
    GPIO.output(GPIO_leftwheel, True)
    GPIO.output(GPIO_leftwheelDIR, False)
    GPIO.output(GPIO_rightwheel, False)
    GPIO.output(GPIO_rightwheelDIR, True)
    pwmleft.start(GPIO_leftwheelDC)	
    pwmright.start(GPIO_rightwheelDC)	

def left180():
    # left wheel backward, right wheel forward
    GPIO.output(GPIO_leftwheel, False)
    GPIO.output(GPIO_leftwheelDIR, True)
    GPIO.output(GPIO_rightwheel, True)
    GPIO.output(GPIO_rightwheelDIR, False)
    pwmleft.start(GPIO_leftwheelDC)	
    pwmright.start(GPIO_rightwheelDC)	

def turn(angle):
    if not angle:
        angle = 1.5
    stop()
    time.sleep(0.05)
    backward()
    time.sleep(1.5)
    stop()
    time.sleep(0.05)
    if angle < 0:
        left180()
    else:
        right180()
    time.sleep(abs(angle))
    stop()
    time.sleep(0.05)
