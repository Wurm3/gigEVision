from aquireimages import AquireImages
from settings import Settings
from led import Led
from button import Button

import RPi.GPIO as GPIO
import time

print("Starting....")
settings = Settings()

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

#Start aquire thread
aquire = AquireImages(settings)
aquire.start()


#Start led thread
status_led = Led(settings, aquire)
status_led.start()

#Start button
button = Button(settings)
button.start()

print("waiting for cleanup...")
aquire.join()
status_led.join()
button.join()
GPIO.cleanup()
print("Finished!")