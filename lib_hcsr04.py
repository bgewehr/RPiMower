__author__ = 'mp911de'


import RPi.GPIO as GPIO
import time
import numpy as np

# GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)
CM_PER_SEC_AIR = 34300

def setup_gpio(gpio_trigger, gpio_echo):
    # Setup GPIO
    global GPIO_TRIGGER 
    global GPIO_ECHO 
    GPIO_TRIGGER = gpio_trigger
    GPIO_ECHO = gpio_echo
    GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
    GPIO.setup(GPIO_ECHO, GPIO.IN)
    global data
    data = []

def percentile_based_outlier(point, threshold=50):

    while len(data) > 5:
        data.pop()

    data.insert(0,point)

    if len(data) < 3:
        return False

    std = np.std(np.array(data).astype(np.float))

    return std < threshold

def get_distance_value():
    # Trigger High
    GPIO.output(GPIO_TRIGGER, True)
    # Trigger after 0.01ms to low
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
    sonicSent = time.time()
    while GPIO.input(GPIO_ECHO) == 0:
        sonicSent = time.time()
    while GPIO.input(GPIO_ECHO) == 1:
        pass
    echoReceived = time.time()
    elapsed = echoReceived - sonicSent
    distance = (elapsed * CM_PER_SEC_AIR) / 2
    return distance

def get_distance():
    distance = get_distance_value()
    while not percentile_based_outlier(distance):
        distance = get_distance_value()
    return distance


def cleanup():
    GPIO.cleanup()

