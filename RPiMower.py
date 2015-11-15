#!/usr/bin/env python

__author__ = "Bernd Gewehr"

# import python libraries
import logging
import os
import signal
import sys
import time
import random
import numpy as np

# import RPiMower actions
import lib_l298n as move
import act_uln2003 as VSS
import act_esc as ESC

# import RPiMower libraries
import lib_mqtt as MQTT

# Initialize variables
APPNAME = os.path.splitext(os.path.basename(__file__))[0]
LOGFILE = os.getenv('LOGFILE', APPNAME + '.log')

DEBUG = True

MQTT_TOPIC_IN = "/RPiMower/#"
MQTT_QOS = 0

STOP = "/RPiMower/stop"
START = "/RPiMower/start"
TURN = "/RPiMower/turn"
HOME = "/RPiMower/return"

Stop = False

MIN_DISTANCE = 20

WORLD = ["FrontUS",0,"BackUS",0,"GroundColour",0, "Compass",0, "Pitch",0, "Roll",0, "map",[]]
W_FRONT_SONAR = 1
W_BACK_SONAR = 3
W_GROUND_COLOUR = 5
W_COMPASS = 7
W_PITCH = 9
W_ROLL = 11
W_MAP = 13

data=[]

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
    
    # if DEBUG:
    #     print msg.topic 
    #     print msg.payload

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

    if msg.topic == HOME:
        logging.debug("RPiMower return...")
        print ("RPiMower return...")
        return_home()
        return


        
    topicparts = msg.topic.split("/")
    
    # if DEBUG:
    #    for i in range(0,len(topicparts)-1):
    #        print i, topicparts[i]
	
    if topicparts[2] == "FrontUS":
        WORLD[W_FRONT_SONAR] = msg.payload

    if topicparts[2] == "Ground_Colour":
        WORLD[W_GROUND_COLOUR] = msg.payload

    if topicparts[2] == "Compass":
        WORLD[W_COMPASS] = int(float(msg.payload))

    if topicparts[2] == "Pitch":
        WORLD[W_PITCH] = int(float(msg.payload))

    if topicparts[2] == "Roll":
        WORLD[W_ROLL] = int(float(msg.payload))
        
# End of MQTT callbacks


def cleanup(signum, frame):
    """
    Signal handler to ensure we disconnect cleanly
    in the event of a SIGTERM or SIGINT.
    """
    # Cleanup  modules
    logging.debug("Clean up modules")
    move.cleanup()
    VSS.cleanup()
    MQTT.cleanup()

    # Exit from application
    logging.info("Exiting on signal %d" % (signum))
    sys.exit(signum)


def detect_blocking(point):
    while len(data) > 10:
        data.pop()

    data.insert(0,point)

    if len(data) < 3:
        return False

    std = np.std(np.array(data).astype(np.float))
    print std, data
    return std < 0.2

def compass_turn(target):
    DC = 90
    while 352 > abs(target - WORLD[W_COMPASS]) > 8:
        print "from - to: ", WORLD[W_COMPASS], target
        if WORLD[W_COMPASS] < target:
            if abs(WORLD[W_COMPASS] - target)<180:
                #Rechtsrum ist kuerzester Weg
                move.right180(DC, DC)
            else:
                #Linksrum ist kuerzester Weg
                move.left180(DC, DC)
        else:
            if abs(WORLD[W_COMPASS] - target)<180:
                #Linksrum ist kuerzester Weg
                move.left180(DC, DC)
            else:
                #Rechtsrum ist kuerzester Weg
                move.right180(DC, DC)
        time.sleep(0.02)
        move.stop()
        time.sleep(0.02)

def build_map():
    global WORLD
    global Stop
    move.stop()
    # wait for the first real compass result
    time.sleep(2)
    current_angle = WORLD[W_COMPASS]
    print "Starting at angle: ", current_angle
    for angle in range(current_angle, current_angle + 359, 2):
        if angle > 360:
            target = angle - 360
        else:
            target = angle
        print "Turning to angle: ", target
        compass_turn(target)
        print "World Map: ", target, WORLD[W_FRONT_SONAR]
        WORLD[W_MAP].append([target, float(WORLD[W_FRONT_SONAR])+47])
    #print WORLD[W_MAP]
    WORLD_CARTESIAN = [[int(np.cos(np.radians(i[0]))*float(i[1])*10)/10, int(np.sin(np.radians(i[0]))*float(i[1])*10)/10] for i in WORLD[W_MAP]]
    #print WORLD_CARTESIAN
    MQTT.mqttc.publish("/RPiMower/World/Cartesian", str(WORLD_CARTESIAN))
    move.stop()

def return_home():
    global Stop
    move.stop()
    time.sleep(0.5)
    move.backward()
    time.sleep(0.5)
    move.stop()
    compass_turn(5)
    move.forward()
    time.sleep(0.5)
    move.stop()
    Stop = true

def mow():
    """
    The main loop in which we mow the lawn.
    """
    blocking = False
    running = False
    k = 0
    while True:
        time.sleep(0.08)
        blocking = detect_blocking(WORLD[W_FRONT_SONAR])
        k = k + 1
        if k == 10:
            #if DEBUG:
            print WORLD[W_FRONT_SONAR], WORLD[W_GROUND_COLOUR], blocking
            #MQTT.mqttc.publish("/RPiMower/World/Polar", str(WORLD[W_MAP]), qos=0, retain=True)
            MQTT.mqttc.publish("/RPiMower/World/Compass", str(WORLD[W_COMPASS]), qos=0, retain=True)
            MQTT.mqttc.publish("/RPiMower/World/FrontUS", str(WORLD[W_FRONT_SONAR]), qos=0, retain=True)
            #MQTT.mqttc.publish("/RPiMower/World/BackUS", WORLD[WORLD_BACK_SONAR], qos=0, retain=True)
            MQTT.mqttc.publish("/RPiMower/World/GroundColour", WORLD[W_GROUND_COLOUR], qos=0, retain=True)
            k = 1
        if Stop and running:
            move.stop()
            print "Stopping..."
            running = False
            VSS.off([5])
            ESC.setThrottle(7.5)
        elif not running:
            move.forward()
            VSS.on([5])
            ESC.setThrottle(8)
            print "Running forward"
            running = True

        if abs(WORLD[W_PITCH])>25:
            print "Stopping mower, RPiMower pitched at ", WORLD[PITCH]
            ESC.setThrottle(7.5)

        if abs(WORLD[W_ROLL])>25:
            print "Stopping mower, RPiMower rolled at ", WORLD[PITCH]
            ESC.setThrottle(7.5)

        if blocking or (float(WORLD[W_FRONT_SONAR]) < MIN_DISTANCE) or (WORLD[W_GROUND_COLOUR] == "blue"):
            print WORLD[W_FRONT_SONAR], WORLD[W_GROUND_COLOUR], blocking
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
ESC.init(12)
MQTT.init()
MQTT.mqttc.on_message = on_message
MQTT.mqttc.subscribe(MQTT_TOPIC_IN, qos=MQTT_QOS)

# start main procedure
build_map()
mow()
