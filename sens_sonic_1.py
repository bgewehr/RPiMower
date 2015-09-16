__author__ = 'Bernd Gewehr'

import time
import os
# import lib_MQTT as MQTT

from lib_distancemeter import setup_gpio, get_distance, cleanup

DEBUG = False

def init():
    # os.nice(10)
    # MQTT.init()
    global WORLD
    setup_gpio(20,19)
    while True:
        time.sleep(0.1)
        distance = get_distance()
        if DEBUG:
            print ("Received distance = %.1f cm" % distance)
        # MQTT.mqttc.publish("/RPiMower/FrontUS", distance)
        WORLD[WORLD_FRONT_US] = distance


def cleanup():
    print "sonic_1 cleanup"
    MQTT.cleanup()

# main
init()
