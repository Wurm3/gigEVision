from settings import Settings
from aquireimages import AquireImages
from retrievedht11 import RetrieveDHT11

import time

print("Starting....")
settings = Settings()

dht11 = RetrieveDHT11(settings)
result_map = dht11.get_data()
if result_map["valid"]:
    print("Temperature: " + str(result_map["temperature"]))
    print("Humidity: " + str(result_map["humidity"]))
else:
    print("No results obtained")
    print(result_map)

"""
#Start aquire thread
aquire = AquireImages(settings)
aquire.start()

settings.PICTURE_MODE = True
time.sleep(10)
settings.PICTURE_MODE = False
time.sleep(2)
settings.running = False
aquire.join()
"""