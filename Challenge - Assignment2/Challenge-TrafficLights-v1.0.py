#################################################################
#								                                #
#			XAMK IoT - Assignment2 - Traffic Lights             #
#			                                                    #
#   								     Eimantas Mažeika 2021  #
#################################################################
import RPi.GPIO as GPIO
from time import sleep
from enum import Enum

# Pin configuration for a button and 3 LEDs
BUTTON_PIN = 26
RED_LED_PIN = 6
YELLOW_LED_PIN = 13
GREEN_LED_PIN = 19

GPIO.setmode(GPIO.BCM)		                # Use Broadcom SoC pin numbering

GPIO.setup(BUTTON_PIN, GPIO.IN)	            # Set pin as an input
GPIO.setup(RED_LED_PIN, GPIO.OUT)	        # Set pin as an output
GPIO.setup(YELLOW_LED_PIN, GPIO.OUT)	    # Set pin as an output
GPIO.setup(GREEN_LED_PIN, GPIO.OUT)	        # Set pin as an output


class operatingMode(Enum):                  # Describe all of the possible operating modes
    GREEN = 1   
    SWITCH = 2
    RED = 3


previousState = 1                           # Track the previous state
operatingState = 1                          # start the program with green light


def button_pressed_callback(channel):       # Function for Button Interrupt 
    print("[LOG] Button pressed!")

    global operatingState, previousState

    #If the light is change'ing inform the user to wait:
    if (operatingState == operatingMode.SWITCH.value):
        print("[LOG] The light is changing, please wait")
    # If the Light is not changing state, initiate the change:
    else:
        previousState = operatingState
        operatingState = operatingMode.SWITCH.value
        print("[LOG] Light change initiated")
    

# Main logic function used to change different states
def TrafficLight():
    global operatingState, previousState

    if(operatingState == operatingMode.GREEN.value):
        GPIO.output(GREEN_LED_PIN, 1)
        GPIO.output(YELLOW_LED_PIN, 0)
        GPIO.output(RED_LED_PIN, 0)

    elif(operatingState == operatingMode.RED.value):
        GPIO.output(GREEN_LED_PIN, 0)
        GPIO.output(YELLOW_LED_PIN, 0)
        GPIO.output(RED_LED_PIN, 1)

    elif(operatingState == operatingMode.SWITCH.value):
        GPIO.output(GREEN_LED_PIN, 0)
        GPIO.output(RED_LED_PIN, 0)

        for cur in range (0, 5):
            GPIO.output(YELLOW_LED_PIN, 1)
            sleep(0.5)
            GPIO.output(YELLOW_LED_PIN, 0)
            sleep(0.5)
        
        if(previousState == operatingMode.RED.value):
            operatingState = 1
        else:
            operatingState = 3


# Attach an interrupt to Button pin on the falling edge (release of the button)
# On interrupt event, call "button_pressed_callback" function
# bouncetime of 100ms saves us from cheap switches, that can generate multiple falling edges.
GPIO.add_event_detect(BUTTON_PIN, GPIO.FALLING, callback=button_pressed_callback, bouncetime=100)


#main loop of the program
while(1):
    TrafficLight()
    sleep(0.05)