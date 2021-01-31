#################################################################
#                                                               #
#                       PIR Example                             #
#               Code by: Eimantas Mazeika 2021                  #
#                                                               #
#################################################################
import RPi.GPIO as GPIO
import datetime
from time import sleep

#Config:
PIR_pin = 4                     # Connect PIR sensor to GPIO 4
time_sleep = 0.1                # Delay cycle by 0.1 seconds

GPIO.setmode(GPIO.BCM)          # Use Broadcom SoC pin numbering
GPIO.setup(PIR_pin, GPIO.IN)    # Set PIR pin as an input

last_pir_state = 0
last_change_datetime = datetime.datetime.now()

while True:
  current_pir_state = GPIO.input(PIR_pin)

  if(last_pir_state != current_pir_state):      # if we detect a state change
      last_pir_state = current_pir_state
      time_now = datetime.datetime.now();
      time_formated = time_now.strftime("%Y-%m-%d %H:%M:%S")

      if(current_pir_state == 1):               # if we detect rising edge
        print("[" + time_formated + " LOG] Motion detected!")
      else:                                     # if we detect falling edge
        motion_time = str((time_now - last_change_datetime).total_seconds())
        print("[" + time_formated + " LOG] Sector is clear! Motion was detected for " + motion_time + "s.")
      last_change_datetime = time_now

  sleep(time_sleep)

