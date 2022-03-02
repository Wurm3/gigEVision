import RPi.GPIO as GPIO
from threading import Thread

class Button(Thread):

    def __init__(self, settings):
        self.settings = settings
        Thread.__init__(self)
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.settings.BUTTON_PIN, pull_up_down=GPIO.PUD_DOWN)

    def toggle_button(self):
        self.settings.PICTURE_MODE = (False, True)[self.settings.PICTURE_MODE]

    def run(self):
        while self.settings.running:
            print(GPIO.input(self.settings.BUTTON_PIN))
            if GPIO.input(self.settings.BUTTON_PIN) == GPIO.HIGH:
                self.toggle_button()
