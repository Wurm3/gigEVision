from pypylon import pylon
from simple_pyspin import Camera
from PIL import Image

import time
import platform
import os

def save_image(img,n):
    output_dir = './images/thermal_images'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    print('Saving to "%s"' % output_dir)

    # Save them
    Image.fromarray(img).save(os.path.join(output_dir, '%08d.jpg' % n))

num_img_to_save = 5
img = pylon.PylonImage()
tlf = pylon.TlFactory.GetInstance()

cam = pylon.InstantCamera(tlf.CreateFirstDevice())
cam.Open()
with Camera() as flir_cam:
    flir_cam.PixelFormat = "Mono8"

    # Get images from the full sensor
    flir_cam.OffsetX = 0
    flir_cam.OffsetY = 0
    flir_cam.Width = flir_cam.SensorWidth
    flir_cam.Height = flir_cam.SensorHeight

    print('Recording...')



    for i in range(num_img_to_save):
        cam.StartGrabbing()

        flir_cam.start()
        flir_array = flir_cam.get_array()
        flir_cam.stop()

        with cam.RetrieveResult(2000) as result:

            # Calling AttachGrabResultBuffer creates another reference to the
            # grab result buffer. This prevents the buffer's reuse for grabbing.
            img.AttachGrabResultBuffer(result)

            if platform.system() == 'Windows':
                # The JPEG format that is used here supports adjusting the image
                # quality (100 -> best quality, 0 -> poor quality).
                ipo = pylon.ImagePersistenceOptions()
                quality = 70
                ipo.SetQuality(quality)

                filename = "saved_pypylon_img_%d.jpeg" % i
                img.Save(pylon.ImageFileFormat_Jpeg, filename, ipo)
            else:
                filename = "saved_pypylon_img_%d.png" % i
                img.Save(pylon.ImageFileFormat_Png, filename)

            # In order to make it possible to reuse the grab result for grabbing
            # again, we have to release the image (effectively emptying the
            # image object).
            img.Release()

        cam.StopGrabbing()
        save_image(flir_array, i)
        print(str(i))
        time.sleep(3)



cam.Close()
