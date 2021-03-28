import sys
sys.path.append("c:\\users\\eiman\\appdata\\local\\packages\\pythonsoftwarefoundation.python.3.9_qbz5n2kfra8p0\\localcache\\local-packages\\python39\\site-packages")

from gpiozero import LED
from gpiozero.pins.pigpio import PiGPIOFactory
from time import sleep

factory = PiGPIOFactory(host='192.168.1.4') #replace the IP with the Raspberry Pi’s IP
 
led = LED(19, pin_factory=factory)

while True:
    led.on()
    sleep(1)
    led.off()
    sleep(1)
