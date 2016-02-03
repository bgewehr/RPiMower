# RPiMower

This is my python project for a robot that can possibly mow the lawn some days.

it consists of 

## Hardware
- a raspberry pi 2 B+
- a raspberry pi camera
- a l298 motor controller
- a 11.1V LiPo battery
- an ultrasonic sensor SD04
- a compass device hmc5883L


## Software
- raspian wheezy
- mosquitto MQTT broker
- some python MQTT daemons for the sensors, running as seperate python tasks
- a python daemon which subscribes to the sensors via MQTT and controls the robot according to the Sensor data

The main idea is to have a world describing variable in the main program which gets sensor data by subscribing to the sensors channels on the MQTT broker on the same machine. Therefore the sensors push their data as often as possible to the MQTT broker and they don't care what happens after sending them out. 

This way I got a high resolution parallel working sensor network with low complexity and cpu consumption.

![https://cloud.githubusercontent.com/assets/4056277/12776336/75598158-ca55-11e5-944a-5f90df71efbf.jpeg](Foto)
