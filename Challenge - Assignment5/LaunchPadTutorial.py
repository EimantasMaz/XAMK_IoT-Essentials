import pygame.mixer
from pygame.mixer import Sound
from gpiozero import Button
from signal import pause

#create an object for the mixer module that loads and plays sounds
pygame.mixer.init() 

#assign each button to a drum sound 
button_sounds = { 
    Button(2): Sound("samples/00 - samples - drum cymbal open.wav"),
    Button(3): Sound("samples/00 - samples - drum heavy kick.wav"),
    Button(14): Sound("samples/00 - samples - drum snare hard.wav"),
    Button(15): Sound("samples/00 - samples - drum cymbal closed.wav"),
}

#the sound plays when the button is pressed
for button, sound in button_sounds.items():
    button.when_pressed = sound.play

#keep the program running to detect events
pause()
