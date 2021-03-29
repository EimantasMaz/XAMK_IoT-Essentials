import tkinter as tk
from time import sleep

root = tk.Tk()
root.title('The Weather App')
root.geometry("350x280")

global dht_temperature, dht_humidity

temp_var = tk.StringVar()
humd_var = tk.StringVar()

temperature_label = tk.Label(root, text = 'Temperature: ')
humidity_label = tk.Label(root,    text = 'Humidity: ')
temp_var_label = tk.Label(root, textvariable=temp_var)
humd_var_label = tk.Label(root, textvariable=humd_var)

def dht_update():
    print("To Be Implemented")
    temp_var.set("update")
    root.after(2000, dht_update)

temperature_label.place(x=20, y=10)
humidity_label.place(x=20, y=30)
temp_var_label.place(x=100, y=10)
humd_var_label.place(x=100, y=30)


#Start the main tkinter loop
root.after(5000, dht_update)
tk.mainloop()