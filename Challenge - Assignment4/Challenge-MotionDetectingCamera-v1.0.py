#################################################################
#                                                               #
#   XAMK IoT - Assignment4 - Motion Detecting Security Camera   #
#                                                               #
#                                        Eimantas Mažeika 2021  #
#################################################################

import picamera
import datetime
from time import sleep
import RPi.GPIO as GPIO
import os

# CONFIG:
images_dir = "/images"
videos_dir = "/videos"
PIR_pin = 4
time_sleep = 0.1

GPIO.setmode(GPIO.BCM)		              # Use Broadcom SoC pin numbering
GPIO.setup(PIR_pin, GPIO.IN)            # Set PIR pin as an input

camera = picamera.PiCamera()
camera.resolution = (1920, 1080)
camera.annotate_text = 'Security Camera By EimantasM'

def logConsole(text):
  time_now = datetime.datetime.now()
  time_formated = time_now.strftime("%Y-%m-%d %H:%M:%S")
  print("[" + time_formated + " LOG] " + text)

def createFolders():
  cwd = os.getcwd()                       #Get the current working directory(CWD)
  try:
      os.stat(cwd + images_dir)           #check that the image folder exists
  except:
      os.mkdir(cwd + images_dir)          #if not, create one

  try:
      os.stat(cwd + videos_dir)           #check that the video folder exists
  except:
      os.mkdir(cwd + videos_dir)          #if not, create one
    

createFolders()

cwd = os.getcwd() 
img_path = cwd + images_dir + "/"
vid_path = cwd + videos_dir + "/"

last_pir_state = 0

# Main loop
while True:
  current_pir_state = GPIO.input(PIR_pin)

  if(last_pir_state != current_pir_state):      # if we detect a state change
      last_pir_state = current_pir_state
      time_now = datetime.datetime.now()
      time_formated = time_now.strftime("%Y-%m-%d %H:%M:%S")

      if(current_pir_state == 1):               # if we detect rising edge - sensor triggers
        logConsole("Motion detected! Image: " + img_path + "MotionDetected-" + time_formated + ".jpg")

        camera.capture(img_path + "MotionDetected-" + time_formated + ".jpg")
        camera.start_recording(vid_path + "MotionDetected-" + time_formated + ".h264")
        
      else:                                     # if we detect falling edge - sensor doesn't see movement
        motion_time = str((time_now - last_change_datetime).total_seconds())
        logConsole("Sector is clear! Motion was detected for " + motion_time + "s. Stopping the recording")
        camera.stop_recording()
      last_change_datetime = time_now

  sleep(time_sleep)
