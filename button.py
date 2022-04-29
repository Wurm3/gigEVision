import RPi.GPIO as GPIO
from threading import Thread

import time
import os

class Button(Thread):

    def __init__(self, settings):
        self.settings = settings
        Thread.__init__(self)
        #GPIO.setwarnings(False)
        #GPIO.setmode(GPIO.BOARD)
        self.pressed = 0
        GPIO.setup(self.settings.BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    def toggle_button(self):
        if self.settings.PICTURE_MODE:
            self.settings.PICTURE_MODE = False
        else:
            self.settings.PICTURE_MODE = True
        print("toggle mode: " + str(self.settings.PICTURE_MODE))

    def run(self):
        while self.settings.running:
            time.sleep(0.05)
            if GPIO.input(self.settings.BUTTON_PIN) == GPIO.HIGH:
                if self.pressed == 0:
                    self.pressed = time.time()
                else:
                    if time.time() - self.pressed > 5:
                        self.settings.FLASHING = True
            else:
                if self.pressed != 0:
                    duration = time.time() - self.pressed
                    self.pressed = 0
                    if 2 < duration < 5:
                        self.settings.running = False
                    elif duration > 5:
                        self.settings.running = False
                        os.system("bash -c \"sleep 10; shutdown -h now\"")
                    else:
                        self.toggle_button()