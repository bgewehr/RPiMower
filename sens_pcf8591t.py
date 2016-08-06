#!/usr/bin/python

__author__ = 'Bernd Gewehr'

import time

import lib_mqtt as MQTT
import os
import sys

#Read a value from analogue input 0-3 and publish to mqtt
#in A/D in the PCF8591t @ address 0x48
from smbus import SMBus
bus = SMBus(1)

DEBUG = True

address = 0x48

def writeAOUT(val):
    val = int(val) # convert to integer
    bus.write_byte_data(address, 0x40, val)

if __name__ == '__main__':
    os.nice(10)
    try:
        MQTT.init()
        last_reading =-1
        last_reading1 =-1
        last_reading2 =-1
        last_reading3 =-1

        for i in [1,255,1]:
            writeAOUT(i)

        while True:
            time.sleep(0.1)

            bus.write_byte(address, 0x40) # set control register to read channel 0

            reading = bus.read_byte(address) # read A/D for starting AD conversion
            reading = bus.read_byte(address) # read A/D value
            if(abs(last_reading - reading) > 2):
                last_reading = reading
                MQTT.mqttc.publish("/RPiMower/World/PowerM1", reading)
            if DEBUG:
                print("1:",reading)

            bus.write_byte(address, 0x41) # set control register to read channel 1

            reading = bus.read_byte(address) # read A/D for starting AD conversion
            reading = bus.read_byte(address) # read A/D value
            if(abs(last_reading1 - reading) > 2):
                last_reading1 = reading
                MQTT.mqttc.publish("/RPiMower/World/PowerM2", reading)
            if DEBUG:
                print("2:",reading)

            bus.write_byte(address, 0x42) # set control register to read channel 3

            reading = bus.read_byte(address) # read A/D for starting AD conversion
            reading = bus.read_byte(address) # read A/D value
            if(abs(last_reading2 - reading) > 2):
                last_reading2 = reading
                MQTT.mqttc.publish("/RPiMower/World/PowerM3", reading)
            if DEBUG:
                print("3:",reading)

            bus.write_byte(address, 0x43) # set control register to read channel 3

            reading = bus.read_byte(address) # read A/D for starting AD conversion
            reading = bus.read_byte(address) # read A/D value
            if(abs(last_reading3 - reading) > 2):
                last_reading3 = reading
                MQTT.mqttc.publish("/RPiMower/World/PowerM4", reading)
            if DEBUG:
                print("4:",reading)

    # interrupt
    except KeyboardInterrupt:
        print("Programm interrupted")
        MQTT.cleanup()
        sys.exit(2)

