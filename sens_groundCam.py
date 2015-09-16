__author__ = 'mp911de'

import time
import os
import picamera
import picamera.array
import time
from math import sqrt, atan2, degrees

# import lib_MQTT as MQTT

DEBUG = False

def get_colour_name(rgb):
    rgb = rgb / 255
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
    if DEBUG:
        print rgb, hue, colour
    return colour

def init():
    # os.nice(10)
    # MQTT.init()
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
                     RGBavg = stream.array.mean(axis=0).mean(axis=0)
                     colour = get_colour_name(RGBavg)
                     # MQTT.mqttc.publish("/RPiMower/Ground_Color", colour)
                     WORLD[WORLD_GROUND_COLOR] = colour

def cleanup():
        print "groundCam cleanup"
        camera.stop_preview()
        # MQTT.cleanup()

# main
init()
