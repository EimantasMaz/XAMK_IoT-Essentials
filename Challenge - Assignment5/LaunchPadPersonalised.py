#################################################################
#                                                               #
#        XAMK IoT - Assignment5 - Electronic Drums set          #
#                                                               #
#                                        Eimantas Mažeika 2021  #
#################################################################

import pygame.mixer
from pygame.mixer import Sound
from gpiozero import Button
from signal import pause

#create an object for the mixer module that loads and plays sounds
pygame.mixer.init() 

#Personalised my sounds to a guitar
button_sounds = { 
    Button(2): Sound("samples/00 - samples - guit harmonics.wav"),
    Button(3): Sound("samples/00 - samples - guit em9.wav"),
    Button(14): Sound("samples/00 - samples - guit e slide.wav"),
    Button(15): Sound("samples/00 - samples - guit e fifths.wav"),
}

#the sound plays when the button is pressed
for button, sound in button_sounds.items():
    button.when_pressed = sound.play

#keep the program running to detect events
pause()
