import socket
import pygame
import time
import webbrowser

pygame.init()
ring = pygame.mixer.Sound("audio/doorbell-1.wav")


client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP 
client.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1) 
client.bind(("", 37020)) 
while True: 
    data, addr = client.recvfrom(1024) 
    print("received message: %s"%data)
    ring.play()
    print("sound played")
    webbrowser.open(data.decode('UTF-8'))
    print("browser opened")


