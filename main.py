from aquireimages import AquireImages
from settings import Settings
from led import Led
from button import Button

import time

print("Starting....")
settings = Settings()


#Start aquire thread
aquire = AquireImages(settings)
aquire.start()


#Start led thread
status_led = Led(settings, aquire)
status_led.start()

#Start button
button = Button(settings)
button.start()

print("waiting...")
time.sleep(20)
settings.running = False

print("Cleanup...")
aquire.join()
status_led.join()
button.join()
print("Finished!")