##########################################################################
#                                                                        #
#           XAMK IoT - Assignment13 - DHT22 Weather App w/Tkinter        #
#                                                                        #
#                                                 Eimantas Mažeika 2021  #
##########################################################################
import tkinter as tk
from time import sleep
import adafruit_dht
from PIL import Image, ImageTk

sensor = adafruit_dht.DHT22(4)

root = tk.Tk()
root.title('The Weather')
root.geometry("250x70")

temperature_threshold = 25
humidity_threshold = 50

global dht_temperature, dht_humidity

temp_var = tk.StringVar()
humd_var = tk.StringVar()

temperature_label = tk.Label(root, text = 'Temperature: ')
humidity_label = tk.Label(root,    text = 'Humidity: ')
temp_var_label = tk.Label(root, textvariable=temp_var)
humd_var_label = tk.Label(root, textvariable=humd_var)

image1 = Image.open("img/barometer.png")
resized_img = ImageTk.PhotoImage(image1.resize((50,50), Image.ANTIALIAS))
img_label = tk.Label(image=resized_img)
img_label.image = resized_img


def change_icon(temperature, humidity):
    if(temperature > temperature_threshold):
        if(humidity < humidity_threshold):
            image1 = Image.open("img/sun.png")
            resized_img = ImageTk.PhotoImage(image1.resize((50,50), Image.ANTIALIAS))
            img_label.configure(image=resized_img)
            img_label.image = resized_img
        else:
            image1 = Image.open("img/sun-cloud-rain.png")
            resized_img = ImageTk.PhotoImage(image1.resize((50,50), Image.ANTIALIAS))
            
            img_label.configure(image=resized_img)
            img_label.image = resized_img

    else:
        if(humidity < humidity_threshold):
            image1 = Image.open("img/clouds.png")
            resized_img = ImageTk.PhotoImage(image1.resize((50,50), Image.ANTIALIAS))
            
            img_label.configure(image=resized_img)
            img_label.image = resized_img
        else:
            image1 = Image.open("img/cloud-rain.png")
            resized_img = ImageTk.PhotoImage(image1.resize((50,50), Image.ANTIALIAS))
            
            img_label.configure(image=resized_img)
            img_label.image = resized_img

def dht_update():
    try: 
        hum, temp = sensor.humidity, sensor.temperature
        print("temp:", temp, "hum:", hum)

        temp_var.set(str(temp)+"°C")
        humd_var.set(str(hum)+"%")

        change_icon(temp, hum)
    except RuntimeError as error: 
        print(error.args[0])

    
    root.after(2000, dht_update)

def exit():
    root.destroy()

temperature_label.place(x=20, y=10)
humidity_label.place(x=20, y=30)
temp_var_label.place(x=120, y=10)
humd_var_label.place(x=120, y=30)
img_label.place(x=200, y=10)


#Start the main tkinter loop
root.after(5000, dht_update)
tk.mainloop()