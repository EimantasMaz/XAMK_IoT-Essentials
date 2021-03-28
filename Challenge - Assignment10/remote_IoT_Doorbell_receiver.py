import sys
sys.path.append("c:\\users\\eiman\\appdata\\local\\packages\\pythonsoftwarefoundation.python.3.9_qbz5n2kfra8p0\\localcache\\local-packages\\python39\\site-packages")
import socket
import pygame
import time
import webbrowser

pygame.init()
ring = pygame.mixer.Sound("C:\\Users\\eiman\\Documents\\GitHub\\XAMK_IoT-Essentials\\Challenge - Assignment10\\audio\\doorbell-1.wav")


client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP 
client.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1) 
client.bind(("", 37020)) 
while True: 
    data, addr = client.recvfrom(1024) 
    print("received message: %s"%data)
    ring.play()
    print("sound played")
    webbrowser.open("http://" + str(data.decode('UTF-8')), new=1)
    print("browser opened")




