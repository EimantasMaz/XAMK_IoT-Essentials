##########################################################################
#                                                                        #
#           XAMK IoT - Assignment9 - LED Dimmer Switch GUI               #
#                                                                        #
#                                                 Eimantas Mažeika 2021  #
##########################################################################
import RPi.GPIO as GPIO
from time import sleep
from tkinter import * 

ENCODER_DT_PIN = 2
ENCODER_CLK_PIN = 3
ENCODER_BUTTON_PIN = 4
LED_PIN = 19

global duty_cycle
global last_button
global last_value

duty_cycle = 0

step = 2

GPIO.setmode(GPIO.BCM)		                # Use Broadcom SoC pin numbering

GPIO.setup(ENCODER_DT_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(ENCODER_CLK_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(ENCODER_BUTTON_PIN, GPIO.IN)
GPIO.setup(LED_PIN, GPIO.OUT)
led_pwm = GPIO.PWM(LED_PIN, 500)

#close the window 
def close_window(): 
    window.destroy()

#Create a function that gets called when slider position is changed
def change_color(self): 
    global duty_cycle

    duty_cycle = slider.get()
    led_pwm.ChangeDutyCycle(duty_cycle)  # where 0.0 <= dc <= 100.0
    print(self) 

#create window for the Tkinter
window = Tk() 
window.title("Encoder PWM") 
window.geometry("300x100") 

#Create slider for tkinter GUI
slider = Scale(window, from_=0, to=100, resolution = 1.0, orient=HORIZONTAL, 
        label="Duty Cycle", troughcolor="white", length=280, command=change_color)
slider.pack()

counter = 0
last_button = False
clk_last = GPIO.input(ENCODER_CLK_PIN)
dt_last = GPIO.input(ENCODER_DT_PIN) 


def encoder_buttonPress(channel):
    global duty_cycle
    global last_value
    global last_button

    

    if(last_button and duty_cycle == 0):
        duty_cycle = last_value
    else:
        last_value = duty_cycle
        duty_cycle = 0

    last_button = True

    
    print(duty_cycle)
    led_pwm.ChangeDutyCycle(duty_cycle)  # where 0.0 <= dc <= 100.0

def encoder_increase():
    global duty_cycle
    global last_value
    global last_button

    last_button = False

    if(duty_cycle + step > 100):
        duty_cycle = 100
    else:
        duty_cycle = duty_cycle + step

def encoder_decrease():
    global duty_cycle
    global last_value
    global last_button

    last_button = False

    if(duty_cycle - step < 0):
        duty_cycle = 0
    else:
        duty_cycle = duty_cycle - step

#If we detect rotation of the encoder, we change brightness of the LED:
def encoder_clk_change(channel):
    global clk_last
    global slider
    
    clkState = GPIO.input(ENCODER_CLK_PIN)
    dtState = GPIO.input(ENCODER_DT_PIN)
    if clkState != clk_last:
        if dtState != clkState:
                encoder_increase()
        else:
                encoder_decrease()

        print(duty_cycle)
        led_pwm.ChangeDutyCycle(duty_cycle)  # where 0.0 <= dc <= 100.0
        slider.set(duty_cycle)

    clk_last = clkState

#Configure interrupts 
GPIO.add_event_detect(ENCODER_BUTTON_PIN, GPIO.FALLING, callback = encoder_buttonPress, bouncetime=100)
GPIO.add_event_detect(ENCODER_CLK_PIN, GPIO.BOTH, callback = encoder_clk_change, bouncetime=10)

#Start the PWM from LED completelly off
led_pwm.start(0)

# Start the Tkinter GUI loop
mainloop()