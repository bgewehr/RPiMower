#!/usr/bin/env python

__author__ = "Bernd Gewehr"

# import python libraries
import logging
import os
import threading
import signal
import sys
import time
import random

# import RPiMower actions
import act_move as move
import act_VSS as VSS

# import RPiMower libraries
import lib_MQTT as MQTT

# import RPiMower sensors
# import sens_sonic_1
# import sens_groundCam

# Initialize variables
APPNAME = os.path.splitext(os.path.basename(__file__))[0]
LOGFILE = os.getenv('LOGFILE', APPNAME + '.log')

DEBUG = True

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


# sensors

# front ultrasonic
def sens_front_us_init():
    from lib_distancemeter import setup_gpio, get_distance, cleanup    
    global WORLD
    setup_gpio(20,19)
    while True:
        time.sleep(0.1)
        distance = get_distance()
        WORLD[WORLD_FRONT_US] = distance
    cleanup()

# ground camera
def sens_groundCam_init():
    import picamera
    import picamera.array
    import time
    from math import sqrt, atan2, degrees
    global camera
    global WORLD
    while True:
        with picamera.PiCamera() as camera:
            with picamera.array.PiRGBArray(camera) as stream:
                 camera.start_preview()
                 camera.resolution = (100, 100)
                 for foo in camera.capture_continuous(stream, 'rgb', use_video_port=False, resize=None, splitter_port=0, burst=True):
                     stream.truncate()
                     stream.seek(0)
                     rgb = stream.array.mean(axis=0).mean(axis=0)
                     rbg = rgb / 255
                     alpha = (2 * rgb[0] - rgb[1] - rgb [2])/2
                     beta = sqrt(3)/2*(rgb[1] - rgb[2])
                     hue = degrees(atan2(beta, alpha))
                     if hue < 0:
                         hue = hue + 360
                     if (hue > 40.0) and (hue <= 150.0):
                         colour = "green"
                     elif (hue > 150.0) and (hue <= 300.0):
                         colour = "blue"
                     else:
                         colour = "red"
                     WORLD[WORLD_GROUND_COLOR] = colour
                     time.sleep(0.5)
                 camera.stop_preview()

# handle incoming MQTT messages
def on_message(mosq, obj, msg):
    """
    Handle incoming messages
    """
    global Stop 
    
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
        print msg.topic, msg.payload 
    #    for i in range(0,len(topicparts)-1):
    #        print i, topicparts[i]
	
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
    # Cleanup interface modules
    logging.debug("Clean up actions")
    move.cleanup()
    VSS.cleanup()

    logging.debug("Clean up libs")
    MQTT.cleanup()

    # cleanup sensor threads

    # Exit from application
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
        if k == 10000:
            if DEBUG:
                 print WORLD
            #MQTT.mqttc.publish("/RPiMower/World/data", str(WORLD))
            #mqttc.publish("/RPiMower/World/BackUS", WORLD[WORLD_BACK_US], qos=0, retain=True)
            #mqttc.publish("/RPiMower/World/GroundColor", WORLD[WORLD_GROUND_COLOR], qos=0, retain=True)
            k = 1
        if Stop and running:
            move.stop()
            print "Stopping..."
            running = False
            VSS.off([5])
        elif not running:
            move.forward()
            VSS.on([5])
            print "Running forward"
            running = True

        if (float(WORLD[WORLD_FRONT_US]) < MIN_DISTANCE) or (WORLD[WORLD_GROUND_COLOR] == "blue"):
            print WORLD
            print "Front obstacle detected, turning..."
            move.stop()
            VSS.off([5])
            move.turn(random.uniform(-2.0,2.0))
            running = False
    move.stop()
    cleanup()

# Use the signal module to handle signals
for sig in [signal.SIGTERM, signal.SIGINT, signal.SIGHUP, signal.SIGQUIT]:
    signal.signal(sig, cleanup)

# Initialise our libraries
MQTT.init()
MQTT.mqttc.on_message = on_message
MQTT.mqttc.subscribe(MQTT_TOPIC_IN, qos=MQTT_QOS)

# initialize the actors
move.init()
VSS.init([5])

# initialize and thread the sensors
t1 = threading.Thread(group=None, name="frontSonar", args=(), kwargs={}, target = sens_front_us_init)
#t1.Daemon = True
t1.start()

t2 = threading.Thread(group=None, name="GroundCam", args=(), kwargs={}, target = sens_groundCam_init)
#t2.Daemon = True
t2.start()

# start main procedure
mow()
