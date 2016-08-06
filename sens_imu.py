#!/usr/bin/python

__author__ = 'Bernd Gewehr'

import smbus
import time
import sys
import lib_mqtt as MQTT
import lib_imu as imu
import os
from math import degrees

from lib_i2c import i2c_raspberry_pi_bus_number

#bus = smbus.SMBus(i2c_raspberry_pi_bus_number())
bus = smbus.SMBus(1)

imu_controller = imu.IMU(bus, 0x68, 0x1e, "IMU")

imu_controller.set_compass_offsets(-8, -200, -8)

DEBUG = False
#DEBUG = True

if __name__ == '__main__':
    #os.nice(10)
    try:
        MQTT.init()
        while True:
            time.sleep(0.1)
            compass = imu_controller.read_pitch_roll_yaw()
            if DEBUG:
                print ("\rHeading: " + str(degrees(compass[2])))
                print ("\rPitch: " + str(degrees(compass[0])+19))
                print ("\rRoll: " + str(degrees(compass[1])-6.6))

            MQTT.mqttc.publish("/RPiMower/Compass", str(degrees(compass[2])+19))
            MQTT.mqttc.publish("/RPiMower/Pitch", str(degrees(compass[0])-6.6))
            MQTT.mqttc.publish("/RPiMower/Roll", str(degrees(compass[1])))

    # interrupt
    except KeyboardInterrupt:
        print("Programm interrupted")
        MQTT.cleanup()
        sys.exit(2)
