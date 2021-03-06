import time
import adafruit_dht


class DHT22:
    def __init__(self, settings):
        self.settings = settings
        self.last_result = {"valid": False}

    def get_data(self):
        result_map = {}
        instance = adafruit_dht.DHT22(self.settings.SENSOR_PIN, use_pulseio=False)
        try:
            result_map["valid"] = True
            result_map["temperature"] = instance.temperature
            result_map["humidity"] = instance.humidity
            self.last_result = result_map
        except RuntimeError as error:
            result_map["valid"] = False
            if self.last_result["valid"]:
                tmp = result_map
                result_map = self.last_result
                self.last_result = tmp
            time.sleep(0.1)
        except Exception as error:
            instance.exit()
            raise error

        return result_map


