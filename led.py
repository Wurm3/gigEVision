import RPi.GPIO as GPIO
from threading import Thread
import time

class Led(Thread):
    def __init__(self,settings):
        Thread.__init__()
        self.settings = settings
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self.settings.LED_PIN,GPIO.OUT)


    def run(self):
        while self.settings.running:
            GPIO.output(self.settings.LED_PIN, GPIO.HIGH)
            time.sleep(self.settings.BLINK_FREQUENCY)
            if not self.settings.PICTURE_MODE:
                GPIO.output(self.settings.LED_PIN, GPIO.LOW)
                time.sleep(self.settings.BLINK_FREQUENCY)
