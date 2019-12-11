import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522

import time



class Reader():

    def __init__(self):
        self.GPIO = GPIO
        self.GPIO.cleanup()
        self.reader = SimpleMFRC522()
        self.decoration = "\n#--- "


    def clean_GPIO(self):
        print(f"{self.decoration}Programm has been terminated...")
        self.GPIO.cleanup()
        print(f"{self.decoration}GPIO has been cleaned up...")


    def read(self):
        try:
            print(f"{self.decoration}sleeping for 2 seconds")
            time.sleep(2)

            self.reader

            print(f'{self.decoration}scanner initialized')

            id = str(self.reader.read_id())

            print(f'{self.decoration}Scan successfull')

        except:
            return '0x0'
        else:
            self.clean_GPIO()  
            return id

