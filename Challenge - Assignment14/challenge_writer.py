#!/usr/bin/env python
##########################################################################
#                                                                        #
#           XAMK IoT - Assignment14 - NFC Bus Tag Writer                 #
#                                                                        #
#                                                 Eimantas Mažeika 2021  #
##########################################################################

import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
from time import sleep
import json
import datetime

debug_mode = True           #If enabled, will print debug messages to screen

reader = SimpleMFRC522()

new_card = {
    "bal": 00.00,
    "MonthlyValid": "2000-01-01"
}

def LogToConsole(text):
    print("[LOG]    " + text)

def DebugToConsole(text):
    if debug_mode:
        print("[DEBUG]  " + text)


def validateBalanceAddition(balance, addition):
    try:
        balance = float(balance)
        addition = float(addition)

        if(balance + addition > 999.999):
            return False
        elif(addition < 0):
            return False
        else:
            DebugToConsole("Balance addition was validated")
            return True
    
    except:
        DebugToConsole("Got an exception when checking balance")
        return False


while 1:
    sleep(1)

    print("\n\n\n\n\n\n\n\n[LOG] Waiting for card...\n\n")

    id, text = reader.read()

    print("\n\n--------------------------------------------------------------")
    print("                     NEW CARD HAS BEEN READ")
    print("                           " + str(id))
    print("--------------------------------------------------------------")    
    DebugToConsole("Read: "+ str(text))

    try:
        res = json.loads(str(text.replace('\'', '"')))
        test = res["bal"]
        valid_card = True
    except:
        valid_card = False

        
    if valid_card:
        card = res
        LogToConsole("Card already contains a ticket")
        print("------------------------------------------")
        print("Current balance: " + str(card["bal"]))
        print("Valid until:     " + str(card["MonthlyValid"]))
        print("------------------------------------------\n")

        entry = input("Write 1 to add bal, 2 to buy a ticket   ")
        if(entry == "1"):
            entry = input("How much to add?   ")
            try:
                addition = round(float(entry),2)
                if(validateBalanceAddition(card["bal"], addition)):
                    DebugToConsole("Adding to account: "+ str(addition))

                    current_bal = card["bal"]
                    card["bal"] = current_bal + addition       
                    DebugToConsole("Writing: "+ str(card))

                    LogToConsole("Please add your card to write new balance")
                    reader.write(str(card))
                    LogToConsole("Written Succesfully")
                else:
                    LogToConsole("Ballance addition has not been validated. Try again")
            except:
                print("CRASH")

        
        elif(entry == "2"):
            entry = input("How many days to add?   ")
            try:
                days_to_add = int(entry)
                DebugToConsole("Adding: "+ str(days_to_add))
                new_valid_date = str(datetime.datetime.now().date() + datetime.timedelta(days=days_to_add))
                DebugToConsole("New Valid Date: "+ str(new_valid_date))

                card["MonthlyValid"] = str(new_valid_date)

                LogToConsole("Please add your card to write new bal")
                reader.write(str(card))
                LogToConsole("Written Succesfully")
            except:
                print("CRASH")

        else:
            print("[LOG] No valid option has been selected\n")

    else:
        LogToConsole("Card does not contain a ticket")
        LogToConsole("Place your card to format")
        LogToConsole("Writing:  " + str(new_card))
        reader.write(str(new_card))
        LogToConsole("Card has been formatted")
        sleep(1)