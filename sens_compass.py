__author__ = 'Bernd Gewehr'

import time

import lib_mqtt as MQTT
from  lib_hmc5883l import  hmc5883l
import os

DEBUG = False

if __name__ == '__main__':
    os.nice(10)
    try:
        MQTT.init()
        while True:
            time.sleep(0.1)
            compass = hmc5883l(gauss = 4.7, declination = (1,36))
            if DEBUG:
                print ("\rHeading: " + str(compass.heading()))
            MQTT.mqttc.publish("/RPiMower/Compass", str(compass.heading()))

    # interrupt
    except KeyboardInterrupt:
        print("Programm interrupted")
        MQTT.cleanup()
        sys.exit(2)

