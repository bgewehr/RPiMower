#!/usr/bin/env python

__author__ = "Bernd Gewehr"

import logging
import os
import signal
import sys
import time
import random

import move
import VSS
import MQTT

# Initialize variables
APPNAME = os.path.splitext(os.path.basename(__file__))[0]
LOGFILE = os.getenv('LOGFILE', APPNAME + '.log')

DEBUG = False

MQTT_TOPIC_IN = "/RPiMower/#"
MQTT_QOS = 0

STOP = "/RPiMower/stop"
START = "/RPiMower/start"
TURN = "/RPiMower/turn"

Stop = False

MIN_DISTANCE = 20

WORLD = ["FrontUS",0,"BackUS",0,"GroundColor",0]
WORLD_FRONT_US = 1
WORLD_BACK_US = 3
WORLD_GROUND_COLOR = 5

# Initialize logging
LOGFORMAT = '%(asctime)-15s %(levelname)-5s %(message)s'

if DEBUG:
    logging.basicConfig(filename=LOGFILE,
                        level=logging.DEBUG,
                        format=LOGFORMAT)
else:
    logging.basicConfig(filename=LOGFILE,
                        level=logging.INFO,
                        format=LOGFORMAT)

logging.info("Starting " + APPNAME)
logging.info("INFO MODE")
logging.debug("DEBUG MODE")
logging.debug("LOGFILE = %s" % LOGFILE)

def on_message(mosq, obj, msg):
    """
    Handle incoming messages
    """
    global Stop 
    
    if DEBUG:
        print msg.topic 
        print msg.payload

    if msg.topic == START:
        logging.debug("RPiMower start...")
        print ("RPiMower start...")
        Stop = False
        return

    if msg.topic == STOP:
        logging.debug("RPiMower stop...")
        print ("RPiMower stop...")
        move.stop()
        Stop = True
        return

    if msg.topic == TURN:
        logging.debug("RPiMower turn...")
        print ("RPiMower turn...")
        move.turn()
        return
        
    topicparts = msg.topic.split("/")
    
    if DEBUG:
        for i in range(0,len(topicparts)-1):
            print i, topicparts[i]
	
    if topicparts[2] == "FrontUS":
        WORLD[WORLD_FRONT_US] = msg.payload

    if topicparts[2] == "Ground_Color":
        WORLD[WORLD_GROUND_COLOR] = msg.payload
        
# End of MQTT callbacks


def cleanup(signum, frame):
    """
    Signal handler to ensure we disconnect cleanly
    in the event of a SIGTERM or SIGINT.
    """
    # Cleanup our interface modules
    logging.debug("Clean up modules")
    move.cleanup()
    VSS.cleanup()
    MQTT.cleanup()

    # Exit from our application
    logging.info("Exiting on signal %d" % (signum))
    sys.exit(signum)


def mow():
    """
    The main loop in which we mow the lawn.
    """
    running = False
    k = 0
    while True:
        k = k + 1
        if k == 1000:
            if DEBUG:
                print WORLD
            MQTT.mqttc.publish("/RPiMower/World/data", str(WORLD))
            #mqttc.publish("/RPiMower/World/BackUS", WORLD[WORLD_BACK_US], qos=0, retain=True)
            #mqttc.publish("/RPiMower/World/GroundColor", WORLD[WORLD_GROUND_COLOR], qos=0, retain=True)
            k = 1
        if Stop:
            move.stop()
            print "Stopping..."
            running = False
            VSS.off([5])
        elif not running:
            move.forward()
            VSS.on([5])
            print "Running forward"
            running = True

        if (float(WORLD[WORLD_FRONT_US]) < MIN_DISTANCE) or (WORLD[WORLD_GROUND_COLOR] == "blau"):
            print WORLD
            print "Front obstacle detected, turning..."
            move.stop()
            VSS.off([5])
            move.turn(random.uniform(-2.0,2.0))
            running = False
    move.stop()

# Use the signal module to handle signals
for sig in [signal.SIGTERM, signal.SIGINT, signal.SIGHUP, signal.SIGQUIT]:
    signal.signal(sig, cleanup)

# Initialise our libraries
move.init()
VSS.init([5])
MQTT.init()
MQTT.mqttc.on_message = on_message
MQTT.mqttc.subscribe(MQTT_TOPIC_IN, qos=MQTT_QOS)

# start main procedure
mow()
