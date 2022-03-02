from aquireimages import AquireImages
from settings import Settings
from led import Led
from button import Button

import time

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

time.sleep(20)
settings.running = False

aquire.join()
status_led.join()
button.join()