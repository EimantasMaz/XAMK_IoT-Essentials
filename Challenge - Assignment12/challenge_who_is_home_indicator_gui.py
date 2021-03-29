##########################################################################
#                                                                        #
#           XAMK IoT - Assignment12 - Who is Home GUI                    #
#                                                                        #
#                                                 Eimantas Mažeika 2021  #
##########################################################################

import sys
sys.path.append("c:\\users\\eiman\\appdata\\local\\packages\\pythonsoftwarefoundation.python.3.9_qbz5n2kfra8p0\\localcache\\local-packages\\python39\\site-packages")

import tkinter as tk
from time import sleep
from gpiozero import PingServer
import RPi.GPIO as GPIO

#Configure the root tkinter window
root = tk.Tk()
root.title('Who is Home indicator')
root.geometry("380x280")

LED_PIN = 2
led_blink_delay = 0.250

GPIO.setmode(GPIO.BCM)		                # Use Broadcom SoC pin numbering

GPIO.setup(LED_PIN, GPIO.OUT)               # Set LED pin as output

HostList = []

def clearList():
    t.delete(0,'end')

def listUpdate():
    clearList()
    for host in HostList:
        t.insert('end', host)

def addHost():
    host = e1.get()
    if(len(host)==0):
        print("Invalid")
    else:
        HostList.append(host)
        listUpdate()

def delOne():
    try:
        val = t.get(t.curselection())
        if val in HostList:
            HostList.remove(val)
            listUpdate()
    except:
        print("Cannot delete, nothing is selected")

def deleteAll():
    while(len(HostList)!=0):
        HostList.pop()
    listUpdate()

def exit():
    print(HostList)
    root.destroy()

def PingServer_checker():
    print("-----------------------------------------------------")
    print("                 Start Host Checking")
    print("-----------------------------------------------------")
    online_counter = 0

    for host in HostList:
        status = PingServer(host).is_active
        print(host + "   " + str(status))
        if(status):
            online_counter += 1

    for i in range(0, online_counter, 1):
        GPIO.output(LED_PIN, 1)
        sleep(led_blink_delay)
        GPIO.output(LED_PIN, 0)
        sleep(led_blink_delay)

    root.after(10000, PingServer_checker)

def dummytask():
    print("To Be Implemented")

l1 = tk.Label(root, text = 'Who is Home indicator')
l2 = tk.Label(root, text='Enter additional Hosts: ')
e1 = tk.Entry(root, width=21)
t = tk.Listbox(root, height=11, selectmode='SINGLE')
b1 = tk.Button(root, text='Add ip', width=20, command=addHost)
b2 = tk.Button(root, text='Delete', width=20, command=delOne)
b3 = tk.Button(root, text='Delete all', width=20, command=deleteAll)
b4 = tk.Button(root, text='Exit', width=20, command=exit)

l1.place(x=120, y=10)
l2.place(x=20, y=50)
e1.place(x=20, y=80)
b1.place(x=20, y=110)
b2.place(x=20, y=140)
b3.place(x=20, y=170)
b4.place(x=20, y =200)
t.place(x=210, y=50)

#Start the main tkinter loop
root.after(5000, PingServer_checker)
tk.mainloop()