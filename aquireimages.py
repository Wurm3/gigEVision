from pypylon import pylon
from simple_pyspin import Camera
from datetime import datetime
from PIL import Image
import PySpin

from settings import Settings
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

    def run(self):
        print("Aquire running")
        img = pylon.PylonImage()
        tlf = pylon.TlFactory.GetInstance()
        while self.settings.running:
            if self.settings.PICTURE_MODE:
                system = PySpin.System.GetInstance()
                cam_list = system.GetCameras()
                for ID, c in enumerate(cam_list):
                    camPtr = cam_list.GetByIndex(0)
                    print(id)
                    print(c)
                    camPtr.Init()
                    try:
                        result = 0
                        nodemap = camPtr.GetTLDeviceNodeMap()
                    except PySpin.SpinnakerException as ex:
                        print('Error: %s' % ex)
                        result = -1

                cam = pylon.InstantCamera(tlf.CreateFirstDevice())
                cam.Open()
                cam.GevSCPSPacketSize.SetValue(1500)
                cam.GevSCPD.SetValue(2000)
                """
                while self.settings.PICTURE_MODE:
                    timestamp = datetime.now()
                    file_ending = timestamp.strftime("%Y-%m-%d-%H%M%S")
                    cam.StartGrabbingMax(1)
                    with cam.RetrieveResult(2000) as result:

                        # Calling AttachGrabResultBuffer creates another reference to the
                        # grab result buffer. This prevents the buffer's reuse for grabbing.
                        img.AttachGrabResultBuffer(result)
                        print(result.GrabSucceeded())
                        print(result.ErrorCode)
                        print(result.ErrorDescription)

                        filename = "basler_%s.png" % file_ending
                        img.Save(pylon.ImageFileFormat_Png, self.settings.VISIBLE_IMAGES_PATH + filename)

                        # In order to make it possible to reuse the grab result for grabbing
                        # again, we have to release the image (effectively emptying the
                        # image object).
                        img.Release()

                    # save images and repeat
                    # save images and repeat
                    cam.StopGrabbing()

                """
                with Camera() as flir_cam:
                    flir_cam.PixelFormat = "Mono8"

                    # Get images from the full sensor
                    flir_cam.OffsetX = 0
                    flir_cam.OffsetY = 0
                    flir_cam.Width = flir_cam.SensorWidth
                    flir_cam.Height = flir_cam.SensorHeight

                    #Testing
                    flir_cam.GevSCPSPacketSize = 1500
                    flir_cam.GevSCPD = 2000

                    try:
                        result = True
                        if flir_cam.TLDevice.DeviceSerialNumber.GetAccessMode() == PySpin.RO:
                            print("Device serial number: %s" % flir_cam.TLDevice.DeviceSerialNumber.ToString())
                        else:
                            print("Device serial number: unavailable")

                        if PySpin.IsReadable(flir_cam.TLDevice.DeviceDisplayName):
                            print("Device display name: %s" % flir_cam.TLDevice.DeviceDisplayName.ToString())
                        else:
                            print("Device display name: unavailable")
                    except PySpin.SpinnakerException as ex:
                        print("Error: %s" % ex)


                    print('Recording...')

                    while self.settings.PICTURE_MODE:
                        timestamp = datetime.now()
                        file_ending = timestamp.strftime("%Y-%m-%d-%H%M%S")

                        cam.StartGrabbing()

                        # Get flir Image
                        flir_cam.start()
                        flir_array = flir_cam.get_array()
                        flir_cam.stop()

                        # Get Basler Image
                        with cam.RetrieveResult(2000) as result:

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
                        time.sleep(self.settings.IMAGE_PAUSE)

                #cam.close()

        #Wait until pictures needs to be taken
        time.sleep(1)
        print("quitting aquire")