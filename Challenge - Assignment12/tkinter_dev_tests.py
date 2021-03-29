import sys
sys.path.append("c:\\users\\eiman\\appdata\\local\\packages\\pythonsoftwarefoundation.python.3.9_qbz5n2kfra8p0\\localcache\\local-packages\\python39\\site-packages")

import tkinter as tk
from time import sleep
from gpiozero import PingServer

#Configure the root tkinter window
root = tk.Tk()
root.title('Who is Home indicator')
root.geometry("350x280")

global app_running
app_running = True
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
    global app_running
    app_running = False
    print(HostList)
    root.destroy()

def PingServer_checker():
    global app_running

    print("-----------------------------------------------------")
    print("                 Start Host Checking")
    print("-----------------------------------------------------")
    for host in HostList:
        status = PingServer(host).is_active
        print(host + "   " + str(status))


    root.after(2000, PingServer_checker)

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
t.place(x=200, y=50)

#Start the main tkinter loop
root.after(2000, PingServer_checker)
tk.mainloop()