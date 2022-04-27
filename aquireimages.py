from pypylon import pylon
from simple_pyspin import Camera
from datetime import datetime
from PIL import Image
from settings import Settings
from dht22 import DHT22

import PySpin
import threading
import platform
import os
import time


class AquireImages(threading.Thread):

    def __init__(self, settings):
        threading.Thread.__init__(self)
        self.settings = settings
        print("initalized thread")

    def save_image(self, img, n):
        if not os.path.exists(self.settings.INFRARED_IMAGES_PATH):
            os.makedirs(self.settings.INFRARED_IMAGES_PATH)

        print('Saving to "%s"' % self.settings.INFRARED_IMAGES_PATH)

        # Save them
        Image.fromarray(img).save(os.path.join(self.settings.INFRARED_IMAGES_PATH, n + ".png"))

    def save_data(self, map, timestamp):
        with open(self.settings.SENSOR_DATA_PATH, 'a+') as f:
            temp = map["temperature"]
            hum = map["humidity"]
            str = "%s, %-3.1f, %-3.1f\n" % (timestamp, temp, hum)
            f.write(str)

    def run(self):
        print("Aquire running")
        img = pylon.PylonImage()
        tlf = pylon.TlFactory.GetInstance()
        while self.settings.running:
            if self.settings.PICTURE_MODE:
                #Initiate Sensor
                result_map = {}
                result_map["valid"] = False
                dht22 = DHT22(self.settings)


                #Initiate Basler camera
                cam = pylon.InstantCamera(tlf.CreateFirstDevice())
                cam.Open()
                print("Setting value")
                cam.GevSCPSPacketSize.SetValue(1500)
                cam.GevSCPD.SetValue(2500)
                print("Value Set")

                with Camera() as flir_cam:
                    flir_cam.PixelFormat = "Mono8"

                    # Get images from the full sensor
                    flir_cam.OffsetX = 0
                    flir_cam.OffsetY = 0
                    flir_cam.Width = flir_cam.SensorWidth
                    flir_cam.Height = 256#flir_cam.SensorHeight
                    print("Width: %s", str(flir_cam.Width))
                    print("Height: %s", str(flir_cam.Height))

                    #Testing
                    flir_cam.GevSCPSPacketSize = 1500
                    flir_cam.GevSCPD = 2000

                    print('Recording...')

                    while self.settings.PICTURE_MODE:
                        timestamp = datetime.now()
                        file_ending = timestamp.strftime("%Y-%m-%d-%H%M%S")
                        skip = False

                        tmp_map_result = dht22.get_data()
                        if tmp_map_result["valid"]:
                            self.save_data(tmp_map_result, file_ending)
                            result_map = tmp_map_result
                        else:
                            if result_map["valid"]:
                                self.save_data(result_map, file_ending)
                                result_map = tmp_map_result
                            else:
                                skip = True
                                print("Could not read sensor")
                        skip = False
                        if not skip:
                            cam.StartGrabbing()

                            # Get flir Image
                            flir_cam.start()
                            flir_array = flir_cam.get_array()
                            flir_cam.stop()

                            # Get Basler Image
                            with cam.RetrieveResult(10000) as result:

                                if not result.GrabSucceeded():
                                    print(result.ErrorCode)
                                    print(result.ErrorDescription)

                                # Calling AttachGrabResultBuffer creates another reference to the
                                # grab result buffer. This prevents the buffer's reuse for grabbing.
                                img.AttachGrabResultBuffer(result)

                                filename = "basler_%s.png" % file_ending
                                img.Save(pylon.ImageFileFormat_Png, self.settings.VISIBLE_IMAGES_PATH + filename)

                                # In order to make it possible to reuse the grab result for grabbing
                                # again, we have to release the image (effectively emptying the
                                # image object).
                                img.Release()

                            #save images and repeat
                            # save images and repeat
                            cam.StopGrabbing()

                            self.save_image(flir_array, "flir_" + file_ending)
                        else:
                            print("Skipped taking pictures")

                        time.sleep(self.settings.IMAGE_PAUSE)

                #cam.close()

        #Wait until pictures needs to be taken
        time.sleep(1)
        print("quitting aquire")