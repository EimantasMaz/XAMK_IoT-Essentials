##########################################################################
#                                                                        #
#           XAMK IoT - Assignment14 - NFC Bus Tag Reader                 #
#                                                                        #
#                                                 Eimantas Mažeika 2021  #
##########################################################################
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
from time import sleep
import json
import datetime
from dateutil import parser

debug_mode = True           #If enabled, will print debug messages to screen
ticket_price = 1.25
led_delay = 0.4

reader = SimpleMFRC522()

RED_LED_PIN = 3
GREEN_LED_PIN = 5
BUZZER_PIN = 7

GPIO.setmode(GPIO.BOARD)		            # Use Broadcom pin_mode numbering

GPIO.setup(GREEN_LED_PIN, GPIO.OUT)         # Set LED pin as output
GPIO.setup(RED_LED_PIN, GPIO.OUT)           # Set LED pin as output
GPIO.setup(BUZZER_PIN, GPIO.OUT)            # Set BUZZER pin as output




def LogToConsole(text):
    print("[LOG]    " + text)

def DebugToConsole(text):
    if debug_mode:
        print("[DEBUG]  " + text)

def AcceptTicket():
    LogToConsole("Ticket Has been accepted")
    GPIO.output(GREEN_LED_PIN, 1)
    sleep(led_delay)
    GPIO.output(GREEN_LED_PIN, 0)

def RejectTicket():
    GPIO.output(RED_LED_PIN, 1)
    LogToConsole("There is no valid monthly pass nor enough funds for a ticket")

    for i in range(0,4,1):
        GPIO.output(BUZZER_PIN, 1)
        sleep(led_delay/4)
        GPIO.output(BUZZER_PIN, 0)
        sleep(led_delay)
    
    GPIO.output(RED_LED_PIN, 0)



while True:
    GPIO.output(GREEN_LED_PIN, 0)
    GPIO.output(RED_LED_PIN, 0)
    GPIO.output(BUZZER_PIN, 0)    
    print("\n\n\n\n\n\n\n\n\n\n")
    LogToConsole("Waiting for card...")

    id, text = reader.read()

    print("\n\n--------------------------------------------------------------")
    print("                     NEW CARD HAS BEEN READ")
    print("                           " + str(id))
    print("--------------------------------------------------------------")  

    try:
        print(text)
        res = json.loads(str(text.replace('\'', '"')))
        test = res["bal"]
        valid_card = True
        LogToConsole("Valid card")
    except:
        LogToConsole("Invalid Card")
        valid_card = False

    

    if(valid_card):
        ValidMonthlyDate = res["MonthlyValid"]
        currentbalance = res["bal"]
        valid_monthly_pass = False

        if (parser.parse(ValidMonthlyDate).date() > datetime.datetime.now().date()):
            valid_monthly_pass = True
            LogToConsole("Valid Monthly pass has been found")
            AcceptTicket()
        
        elif (float(currentbalance) > ticket_price):
            res["bal"] = currentbalance - ticket_price
            reader.write(str(res))
            LogToConsole("Ticket has been Bought. ticket price has been deducted")
            AcceptTicket()
        else:
            RejectTicket()

        print("------------------------------------------")
        print("           REMAINING CARD STATS")
        print("------------------------------------------")
        print("Current balance:    " + str(res["bal"]))
        print("Valid until:        " + str(res["MonthlyValid"]))
        print("Monthly pass valid: " + str(valid_monthly_pass))
        print("------------------------------------------\n")

    sleep(1)