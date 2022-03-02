import RPi.GPIO as GPIO
from threading import Thread

import time

class Button(Thread):

    def __init__(self, settings):
        self.settings = settings
        Thread.__init__(self)
        #GPIO.setwarnings(False)
        #GPIO.setmode(GPIO.BOARD)
        self.pressed = 0
        GPIO.setup(self.settings.BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    def toggle_button(self):
        print("toggle mode")
        self.settings.PICTURE_MODE = (False, True)[self.settings.PICTURE_MODE]

    def run(self):
        while self.settings.running:
            #print(GPIO.input(self.settings.BUTTON_PIN))
            if GPIO.input(self.settings.BUTTON_PIN) == GPIO.HIGH:
                if self.pressed == 0:
                    self.pressed = time.time()
                    if time.time() - self.pressed > 2:
                        self.settings.running = False
            else:
                if self.pressed != 0:
                    duration = time.time() - self.pressed
                    self.pressed = 0
                    if duration > 2:
                        self.settings.running = False
                    else:
                        self.toggle_button()