import board

class Settings:

    def __init__(self):
        self.LED_PIN = 18
        self.BLINK_FREQUENCY = 0.5
        self.BUTTON_PIN = 15
        self.SENSOR_PIN = board.D4 #Pin number 4

        #flag if currently in picturemode
        self.PICTURE_MODE = False

        #if programm is running
        self.running = True

        #How many seconds to pause between images
        self.IMAGE_PAUSE = 0.5

        #path to visible images
        self.VISIBLE_IMAGES_PATH = "/home/ubuntu/software/gigEVision/images/visible_images/"

        #path to infrared images
        self.INFRARED_IMAGES_PATH = "/home/ubuntu/software/gigEVision/images/thermal_images/"

        #file to sensor data
        self.SENSOR_DATA_PATH = "/home/ubuntu/software/gigEVision/images/sensor_data.csv"

        self.FLASHING = False


