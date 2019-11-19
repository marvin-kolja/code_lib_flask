import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522

import time



class Reader():

    def __init__(self):
        self.GPIO = GPIO
        self.reader = SimpleMFRC522()


    def clean_GPIO(self):
        print("\n\nProgramm has been terminated...")
        self.GPIO.cleanup()
        print("GPIO has been cleaned up...")


    def read(self):
        try:
            print("sleeping")
            time.sleep(20)
            print('ready to scan')

            self.reader

            print('scanner initialized')

            id = self.reader.read_id()

            print('Scan successfull')

        except:
            return '0x0'
        else:
            self.clean_GPIO()  
            data = {'id':id}
            return data

