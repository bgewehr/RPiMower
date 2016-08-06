#!/usr/bin/python

__author__ = 'mp911de'

import time
import os,sys
import picamera
import picamera.array
import time
import numpy as np

import lib_mqtt as MQTT

from math import sqrt, atan2, degrees

DEBUG = False

def get_colour_name(rgb):
    rgb = rgb / 255
    alpha = (2 * rgb[0] - rgb[1] - rgb [2])/2
    beta = sqrt(3)/2*(rgb[1] - rgb[2])
    hue = int(degrees(atan2(beta, alpha)))
    std = np.std(rgb)
    mean = np.mean(rgb)
    if hue < 0:
        hue = hue + 360
    if std < 0.055:
        if mean > 0.85:
            colour = "white"
        elif mean < 0.15:
            colour = "black"
        else:
            colour = "grey"
    elif (hue > 50) and (hue <= 160):
        colour = "green"
    elif (hue > 160) and (hue <= 250):
        colour = "blue"
    else:
        colour = "red"
    if DEBUG:
        print rgb, hue, std, mean, colour
    return colour

if __name__ == '__main__':
    # os.nice(10)
    try:
        MQTT.init()
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
                         MQTT.mqttc.publish("/RPiMower/Ground_Colour", colour)

    # interrupt
    except KeyboardInterrupt:
        print("Programm interrupted")
        camera.stop_preview()
        MQTT.cleanup()
        sys.exit(2)
