import picamera
import picamera.array
import time

dominance = 1.2

with picamera.PiCamera() as camera:
    # camera.brightness = 70
    # camera.sharpness = 0
    # camera.contrast = 0
    # camera.saturation = 0
    # camera.ISO = 0
    camera.video_stabilization = False
    # camera.exposure_compensation = 0
    # camera.exposure_mode = 'auto'
    # camera.meter_mode = 'average'
    # camera.awb_mode = 'auto'
    # camera.image_effect = 'none'
    # camera.color_effects = None
    # camera.rotation = 0
    # camera.hflip = False
    # camera.vflip = False
    # camera.crop = (0.0, 0.0, 1.0, 1.0)

with picamera.PiCamera() as camera:
    with picamera.array.PiRGBArray(camera) as stream:
        camera.start_preview()
        # while True:
        camera.resolution = (100, 100)
        for foo in camera.capture_continuous(stream, 'rgb', use_video_port=False, resize=None, splitter_port=0, burst=True):
            stream.truncate()
            stream.seek(0)
            RGBavg = stream.array.mean(axis=0).mean(axis=0)
            print str(time.time()) + " Mittelwert: " + str(RGBavg)
            if (RGBavg[0] > dominance * RGBavg[1]) and (RGBavg[0] > dominance * RGBavg[2]):
                print "Das Bild scheint rot zu sein!"
            elif (RGBavg[1] > dominance * RGBavg[0]) and (RGBavg[1] > dominance * RGBavg[2]):
                print "Das Bild scheint gruen zu sein!"
            elif ((RGBavg[2] + RGBavg[1]) > 4 * RGBavg[0]):
                print "Das Bild scheint blau zu sein!"
            else:
                print "Das Bild scheint  weiss zu sein!"


