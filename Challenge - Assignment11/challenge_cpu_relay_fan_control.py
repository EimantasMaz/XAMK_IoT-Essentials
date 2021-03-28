##########################################################################
#                                                                        #
#           XAMK IoT - Assignment11 - Fan Relay temp control             #
#                                                                        #
#                                                 Eimantas Mažeika 2021  #
##########################################################################
import RPi.GPIO as GPIO
from gpiozero import CPUTemperature
import time

RELAY_PIN = 2

target_temperature = 45
temperature_delta = 1
measurement_delay = 2.5

GPIO.setmode(GPIO.BCM)		                # Use Broadcom SoC pin numbering

GPIO.setup(RELAY_PIN, GPIO.OUT)

while 1:
    cpu_data = CPUTemperature()
    temp = cpu_data.temperature

    if(temp > (target_temperature + temperature_delta)):
        GPIO.output(RELAY_PIN, 1)
        print("Current temperature is: " + str(temp) + "  Cooling fan: On!")

    elif(temp < (target_temperature - temperature_delta)):
        GPIO.output(RELAY_PIN, 0)
        print("Current temperature is: " + str(temp) + "  Cooling fan: Off")

    else:
        print("Current temperature is: " + str(temp) + " In temp delta mode")

    time.sleep(measurement_delay)