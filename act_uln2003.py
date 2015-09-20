import RPi.GPIO as GPIO

def init(pins):
    # GPIO Mode (BOARD / BCM)
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    # Setup GPIO
    for pin in pins:
        GPIO.setup(pin, GPIO.OUT)

def cleanup():
    GPIO.cleanup()

def on(pins):
    for pin in pins:
        GPIO.output(pin, True)

def off(pins):
    for pin in pins:
        GPIO.output(pin, False)

