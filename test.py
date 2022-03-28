from settings import Settings
from aquireimages import AquireImages
from retrievedht11 import RetrieveDHT11
from button import Button
import RPi.GPIO as GPIO
import time
import adafruit_dht


print("Starting....")
settings = Settings()

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)


"""
button = Button(settings)

button.start()

time.sleep(20)
settings.running = False
button.join()

"""

dht11 = RetrieveDHT11(settings)

retrieve = True
counter = 0

while(retrieve):
    result_map = dht11.get_data()

    if result_map["valid"]:
        print("Temperature: " + str(result_map["temperature"]))
        print("Humidity: " + str(result_map["humidity"]))
    else:
        print("No results obtained")
        print(result_map)
    time.sleep(settings.IMAGE_PAUSE + 1.5)
    counter += 1
    if counter >= 20:
        retrieve = False

dhtDevice = adafruit_dht.DHT22(settings.SENSOR_PIN, use_pulseio=False)

while True:
    try:
        # Print the values to the serial port
        temperature_c = dhtDevice.temperature
        temperature_f = temperature_c * (9 / 5) + 32
        humidity = dhtDevice.humidity
        print(
            "Temp: {:.1f} F / {:.1f} C    Humidity: {}% ".format(
                temperature_f, temperature_c, humidity
            )
        )

    except RuntimeError as error:
        # Errors happen fairly often, DHT's are hard to read, just keep going
        print(error.args[0])
        time.sleep(2.0)
        continue
    except Exception as error:
        dhtDevice.exit()
        raise error

    time.sleep(2.0)


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