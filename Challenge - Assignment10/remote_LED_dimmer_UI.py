##########################################################################
#                                                                        #
#     XAMK IoT - Assignment10 1/3- Remote LED Dimmer Switch GUI          #
#                                                                        #
#                                                 Eimantas Mažeika 2021  #
##########################################################################
import sys # this might not be necesarry if python can succesfully find all the required paths to packages
sys.path.append("c:\\users\\eiman\\appdata\\local\\packages\\pythonsoftwarefoundation.python.3.9_qbz5n2kfra8p0\\localcache\\local-packages\\python39\\site-packages")
from gpiozero.pins.pigpio import PiGPIOFactory
from time import sleep
from gpiozero import PWMLED
from gpiozero import Button
from gpiozero import RotaryEncoder
import tkinter as tk

## CONSTANTS AND PIN DEFINITIONS:
ENCODER_DT_PIN = 2
ENCODER_CLK_PIN = 3
ENCODER_BUTTON_PIN = 4
LED_PIN = 19


factory = PiGPIOFactory(host='192.168.1.4') #replace the IP with the Raspberry Pi’s IP

rotor = RotaryEncoder(ENCODER_CLK_PIN, ENCODER_DT_PIN, wrap=False,        # Rotary encoder connected to GPIO
                        max_steps=50, pin_factory=factory)
button = Button(ENCODER_BUTTON_PIN,pull_up=True, pin_factory=factory)     # Rotary encoder Button connected to GPIO
led = PWMLED(LED_PIN, pin_factory=factory)                                # LED connected to GPIO

rotor.steps = -50

global duty_cycle
global last_button
global last_value

duty_cycle = 0
last_button = False

def encoder_buttonPress(channel):
    global last_value
    global last_button
    global duty_cycle

    if(last_button and duty_cycle == 0):
        duty_cycle = last_value
    else:
        last_value = duty_cycle
        duty_cycle = 0

    last_button = True

    print(duty_cycle)
    rotor.steps = duty_cycle*100-50
    led.value = duty_cycle                    # where 0.0 <= dc <= 100.0

def change_duty_cycle():
    global duty_cycle
    global slider

    duty_cycle = (rotor.steps + 50)/ 100
    print(duty_cycle)
    led.value = duty_cycle
    slider.set(duty_cycle*100)

rotor.when_rotated = change_duty_cycle
button.when_pressed = encoder_buttonPress    # Register the event handler for Encoder Button

#close the window 
def close_window(): 
    window.destroy()

#Create a function that gets called when slider position is changed
def change_color(self): 
    global duty_cycle
    global slider

    duty_cycle = slider.get() / 100
    rotor.steps = duty_cycle * 100 - 50
    led.value = duty_cycle / 100  # where 0.0 <= dc <= 100.0
    print(duty_cycle) 

window = tk.Tk() 
window.title("Encoder PWM") 
window.geometry("300x100") 

slider = tk.Scale(window, from_=0, to=100, resolution = 1.0, orient=tk.HORIZONTAL, 
        label="Duty Cycle", troughcolor="white", length=280, command=change_color)
slider.pack()

tk.mainloop()