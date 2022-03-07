import RPi.GPIO as GPIO
from threading import Thread
import time
from aquireimages import AquireImages

class Led(Thread):
    def __init__(self, settings, aquire):
        Thread.__init__(self)
        self.aquire = aquire
        self.settings = settings
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self.settings.LED_PIN, GPIO.OUT)


    def run(self):
        while self.settings.running:
            if self.aquire.is_alive():
                GPIO.output(self.settings.LED_PIN, GPIO.HIGH)
                time.sleep(self.settings.BLINK_FREQUENCY)
                if not self.settings.PICTURE_MODE:
                    GPIO.output(self.settings.LED_PIN, GPIO.LOW)
                    time.sleep(self.settings.BLINK_FREQUENCY)
            else:
                GPIO.output(self.settings.LED_PIN, GPIO.LOW)
                time.sleep(self.settings.BLINK_FREQUENCY * 3)
                GPIO.output(self.settings.LED_PIN, GPIO.HIGH)
                time.sleep(self.settings.BLINK_FREQUENCY)
        GPIO.output(self.settings.LED_PIN, GPIO.LOW)
