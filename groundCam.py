__author__ = 'mp911de'

import time
import os
import picamera
import picamera.array
import time

import MQTT

DEBUG = False

if __name__ == '__main__':
    # os.nice(10)
    try:
        MQTT.init()
        while True:
            dominance = 1.2
            with picamera.PiCamera() as camera:
                with picamera.array.PiRGBArray(camera) as stream:
                     camera.start_preview()
                     camera.resolution = (100, 100)
                     for foo in camera.capture_continuous(stream, 'rgb', use_video_port=False, resize=None, splitter_port=0, burst=True):
                         stream.truncate()
                         stream.seek(0)
                         RGBavg = stream.array.mean(axis=0).mean(axis=0)
                         if (RGBavg[0] > dominance * RGBavg[1]) and (RGBavg[0] > dominance * RGBavg[2]):
                             color = "rot"
                         elif (RGBavg[1] > dominance * RGBavg[0]) and (RGBavg[1] > dominance * RGBavg[2]):
                             color = "gruen"
                         elif ((RGBavg[2] + RGBavg[1]) > 4 * RGBavg[0]):
                             color = "blau"
                         else:
                             color = "weiss"
                         if DEBUG:
                             print color
                         MQTT.mqttc.publish("/RPiMower/Ground_Color", color)

    # interrupt
    except KeyboardInterrupt:
        print("Programm interrupted")
        camera.stop_preview()
        MQTT.cleanup()
