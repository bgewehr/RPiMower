__author__ = 'Bernd Gewehr'

import time

import MQTT
from distancemeter import setup_gpio, get_distance, cleanup
import os

DEBUG = False

if __name__ == '__main__':
    os.nice(10)
    try:
        MQTT.init()
	setup_gpio(20,19)

        while True:
            time.sleep(0.1)
            distance = get_distance()
            if DEBUG:
                print ("Received distance = %.1f cm" % distance)
            MQTT.mqttc.publish("/RPiMower/FrontUS", distance)

    # interrupt
    except KeyboardInterrupt:
        print("Programm interrupted")
        MQTT.cleanup()
