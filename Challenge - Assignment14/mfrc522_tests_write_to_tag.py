#!/usr/bin/env python

import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522


reader = SimpleMFRC522()

test = {
    "Balance": 15.00,
    "MonthlyValid": "2021-03-30"
}


try:
        text = input('New data:')
        print("Now place your tag to write")
        reader.write(str(test))
        print("Written")
finally:
        GPIO.cleanup()