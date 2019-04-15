from gpiozero import Button
import time

def button_1_pressed():
    print("button 1 pressed")

def button_2_pressed():
    print("button 2 pressed")

def button_3_pressed():
    print("button 3 pressed")

def button_4_pressed():
    print("button 4 pressed")

button1 = Button(3)
button2 = Button(4)
button3 = Button(14)
button4 = Button(2)

button1.when_pressed = button_1_pressed
button2.when_pressed = button_2_pressed
button3.when_pressed = button_3_pressed
button4.when_pressed = button_4_pressed

while True:
    time.sleep(1)
