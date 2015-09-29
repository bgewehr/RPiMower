import RPi.GPIO as GPIO
import time

def init(pin):
    # GPIO Mode (BOARD / BCM)
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    # Setup GPIO
    GPIO.setup(pin, GPIO.OUT)
    global PIN
    PIN = pin
    global pwm
    pwm=GPIO.PWM(pin,50)
    pwm.start(7.5)
    time.sleep(1)
    #pwm.ChangeDutyCycle(11)
    #time.sleep(1)
    #pwm.ChangeDutyCycle(7.5)
    #time.sleep(1)

def cleanup():
    pwm.stop()
    GPIO.cleanup()

def setThrottle(pct):
    pwm.ChangeDutyCycle(pct)

#init(12)
#setThrottle(11)
#time.sleep(5)
#cleanup()
