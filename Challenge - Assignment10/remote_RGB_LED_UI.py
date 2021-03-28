##########################################################################
#                                                                        #
#        XAMK IoT - Assignment10 2/3- Remote RGB LED UI                  #
#                                                                        #
#                                                 Eimantas Mažeika 2021  #
##########################################################################
import sys # this might not be necesarry if python can succesfully find all the required paths to packages
sys.path.append("c:\\users\\eiman\\appdata\\local\\packages\\pythonsoftwarefoundation.python.3.9_qbz5n2kfra8p0\\localcache\\local-packages\\python39\\site-packages")
from gpiozero.pins.pigpio import PiGPIOFactory
from gpiozero import PWMLED # import necessary libraries 
from tkinter import * 
import tkinter

red_slider_modifier = -0.02
green_slider_modifier = 0.01
blue_slider_modifier = -0.03
blue_slider_modifier2 = 0.01

factory = PiGPIOFactory(host='192.168.1.4') #replace the IP with the Raspberry Pi’s IP

#create a PWMLED object for each color 
red =   PWMLED(2, pin_factory=factory) 
green = PWMLED(3, pin_factory=factory) 
blue =  PWMLED(4, pin_factory=factory) 

#create window 
window = Tk() 
window.title("RGB LED Controller") 
window.geometry("300x280") 

textlabel = Label(window, text="To win, please move all sliders\nto their maximum position").place(x=40, y=210)


def set_win():
    textlabel2 = Label(window, text="Victory! You won!").place(x=80, y=250)


#change the RGB LED color 
def change_color_red(self):
    green_slider.set(green_slider.get() + blue_slider.get() * green_slider_modifier)
    blue_slider.set(blue_slider.get() + red_slider.get() * blue_slider_modifier2)

    red.value = red_slider.get() 
    green.value = green_slider.get() 
    blue.value = blue_slider.get()

    if(red.value == 1 and green.value == 1 and blue.value == 1):
        set_win()

    print(self)

def change_color_green(self):
    blue_slider.set(blue_slider.get() + red_slider.get() * blue_slider_modifier)

    red.value = red_slider.get() 
    green.value = green_slider.get() 
    blue.value = blue_slider.get()

    if(red.value == 1 and green.value == 1 and blue.value == 1):
        set_win()

    print(self)

def change_color_blue(self):
    red_slider.set(red_slider.get() + green_slider.get() * red_slider_modifier)
 
    red.value = red_slider.get() 
    green.value = green_slider.get() 
    blue.value = blue_slider.get()

    if(red.value == 1 and green.value == 1 and blue.value == 1):
        set_win()

    print(self)


#close the window 
def close_window(): 
    window.destroy()





#create three sliders to control each RGB LED lead 
red_slider = Scale(window, from_=0, to=1, resolution = 0.01, orient=HORIZONTAL, 
        label="Red", troughcolor="red", length=200, command=change_color_red)
red_slider.pack()

green_slider = Scale(window, from_=0, to=1, resolution = 0.01, orient=HORIZONTAL,
        label="Green", troughcolor="green", length=200, command=change_color_green) 
green_slider.pack() 

blue_slider = Scale(window, from_=0, to=1, resolution = 0.01, orient=HORIZONTAL, 
        label="Blue", troughcolor="blue", length=200, command=change_color_blue) 
blue_slider.pack()

#create close button 
close_button = Button(window, text="Close", command=close_window) 
close_button.pack() 

mainloop()
