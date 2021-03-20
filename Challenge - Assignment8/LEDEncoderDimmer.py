##########################################################################
#								                                         #
#			XAMK IoT - Assignment8 - LED Dimmer Switch                   #
#			                                                             #
#   								              Eimantas Mažeika 2021  #
##########################################################################
import RPi.GPIO as GPIO
from time import sleep

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

counter = 0
clk_last = GPIO.input(ENCODER_CLK_PIN)
dt_last = GPIO.input(ENCODER_DT_PIN) 

last_button = False

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


GPIO.add_event_detect(ENCODER_BUTTON_PIN, GPIO.FALLING, callback = encoder_buttonPress, bouncetime=100)

led_pwm.start(0)

while True:
    clkState = GPIO.input(ENCODER_CLK_PIN)
    dtState = GPIO.input(ENCODER_DT_PIN)
    if clkState != clk_last:
        if dtState != clkState:
                encoder_increase()
        else:
                encoder_decrease()

        print(duty_cycle)
        led_pwm.ChangeDutyCycle(duty_cycle)  # where 0.0 <= dc <= 100.0

    clk_last = clkState