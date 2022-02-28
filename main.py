from aquireimages import AquireImages
from settings import Settings
from led import Led

import time

settings = Settings.__init__()


#Start aquire thread
aquire = AquireImages.__init__(settings)
aquire.start()

#Start led thread
status_led = Led.__init__(settings)
status_led.start()

time.sleep(20)
settings.running = False

aquire.join()
status_led.join()