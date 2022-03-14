import RPi.GPIO as GPIO
from dht11.dht11 import DHT11

class RetrieveDHT11:
    def __init__(self, settings):
        self.settings = settings

    def get_data(self):
        result_map = {}
        instance = DHT11(pin = self.settings.SENSOR_PIN)
        result = instance.read()
        if result.is_valid():
            result_map["valid"] = True
            result_map["temperature"] = result.temperature
            result_map["humidity"] = result.humidity
        else:
            result_map["valid"] = False

        return result_map
