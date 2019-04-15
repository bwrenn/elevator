import RPi.GPIO as GPIO
import time
from gpiozero import Button
from enum import Enum
#from __builtin__ import True

class State(Enum):
    DOWN = 0
    UP = 1
    STATIONARY = 3
    
floor_1 = 0
floor_2 = 1
floor_3 = 2

gpio_elevator_motor_out_1 = 17
gpio_elevator_motor_out_2 = 22
gpio_elevator_motor_out_3 = 18
gpio_elevator_motor_out_4 = 27

gpio_led_floor_1_up_pressed = 9
gpio_led_floor_1_up_arrived = 11
gpio_led_floor_2_dn_pressed = 7
gpio_led_floor_2_dn_arrived = 8
gpio_led_floor_2_up_pressed = 25
gpio_led_floor_2_up_arrived = 10
gpio_led_floor_3_dn_pressed = 24
gpio_led_floor_3_dn_arrived = 23

gpio_button_up_floor_1 = 4
gpio_button_dn_floor_2 = 2
gpio_button_up_floor_2 = 3
gpio_button_dn_floor_3 = 14

button_floor_1_up = Button(gpio_button_up_floor_1)
button_floor_2_dn = Button(gpio_button_dn_floor_2)
button_floor_2_up = Button(gpio_button_up_floor_2)
button_floor_3_dn = Button(gpio_button_dn_floor_3)

stop_at_floor_up = [ False, False, True ]
stop_at_floor_dn = [ True, False, False ]

current_floor = floor_1

current_state = State.STATIONARY

def do_init():
    GPIO.setup(gpio_led_floor_1_up_pressed, GPIO.OUT)
    GPIO.setup(gpio_led_floor_1_up_arrived, GPIO.OUT)
    GPIO.setup(gpio_led_floor_2_dn_pressed, GPIO.OUT)
    GPIO.setup(gpio_led_floor_2_dn_arrived, GPIO.OUT)
    GPIO.setup(gpio_led_floor_2_up_pressed, GPIO.OUT)
    GPIO.setup(gpio_led_floor_2_up_arrived, GPIO.OUT)
    GPIO.setup(gpio_led_floor_3_dn_pressed, GPIO.OUT)
    GPIO.setup(gpio_led_floor_3_dn_arrived, GPIO.OUT)
    
    GPIO.output(gpio_led_floor_1_up_pressed, GPIO.LOW)
    GPIO.output(gpio_led_floor_1_up_arrived, GPIO.LOW)
    GPIO.output(gpio_led_floor_2_dn_pressed, GPIO.LOW)
    GPIO.output(gpio_led_floor_2_dn_arrived, GPIO.LOW)
    GPIO.output(gpio_led_floor_2_up_pressed, GPIO.LOW)
    GPIO.output(gpio_led_floor_2_up_arrived, GPIO.LOW)
    GPIO.output(gpio_led_floor_3_dn_pressed, GPIO.LOW)
    GPIO.output(gpio_led_floor_3_dn_arrived, GPIO.LOW)
    
    button_floor_1_up.when_pressed = button_floor_1_up_pressed
    button_floor_2_dn.when_pressed = button_floor_2_dn_pressed
    button_floor_2_up.when_pressed = button_floor_2_up_pressed
    button_floor_3_dn.when_pressed = button_floor_3_dn_pressed
    
    stop_at_floor_up = [ False, False, True ]
    stop_at_floor_dn = [ True, False, False ]
    
def do_exit():
    GPIO.output(gpio_led_floor_1_up_pressed, GPIO.LOW)
    GPIO.output(gpio_led_floor_1_up_arrived, GPIO.LOW)
    GPIO.output(gpio_led_floor_2_dn_pressed, GPIO.LOW)
    GPIO.output(gpio_led_floor_2_dn_arrived, GPIO.LOW)
    GPIO.output(gpio_led_floor_2_up_pressed, GPIO.LOW)
    GPIO.output(gpio_led_floor_2_up_arrived, GPIO.LOW)
    GPIO.output(gpio_led_floor_3_dn_pressed, GPIO.LOW)
    GPIO.output(gpio_led_floor_3_dn_arrived, GPIO.LOW)

def button_floor_1_up_pressed():
    print("1 up pressed")
    stop_at_floor_dn[floor_1] = True
    GPIO.output(gpio_led_floor_1_up_pressed, GPIO.HIGH)

def button_floor_2_dn_pressed():
    print("2 down pressed")
    stop_at_floor_dn[floor_2] = True
    GPIO.output(gpio_led_floor_2_dn_pressed, GPIO.HIGH)

def button_floor_2_up_pressed():
    print("2 up pressed")
    stop_at_floor_up[floor_2] = True
    GPIO.output(gpio_led_floor_2_up_pressed, GPIO.HIGH)

def button_floor_3_dn_pressed():
    print("3 down pressed")
    stop_at_floor_dn[floor_3] = True
    GPIO.output(gpio_led_floor_3_dn_pressed, GPIO.HIGH)

def go(direction):
    i = 0
    positive = 0
    negative = 0
    y = 0
    x = 50
    
    if State.DOWN == direction & floor_1 == current_floor:
        return
    
    if State.UP == direction & floor_3 == current_floor:
        return
    
    GPIO.output(gpio_elevator_motor_out_1, GPIO.LOW)
    GPIO.output(gpio_elevator_motor_out_2, GPIO.LOW)
    GPIO.output(gpio_elevator_motor_out_3, GPIO.LOW)
    GPIO.output(gpio_elevator_motor_out_4, GPIO.LOW)
    
    if x>0 and x<=400:
        for y in range(x,0,-1):
            if negative==1:
                if i==7:
                    i=0
                else:
                    i=i+1
                y=y+2
                negative=0
            positive=1
            #print((x+1)-y)
            if i==0:
                GPIO.output(gpio_elevator_motor_out_1,GPIO.HIGH)
                GPIO.output(gpio_elevator_motor_out_2,GPIO.LOW)
                GPIO.output(gpio_elevator_motor_out_3,GPIO.LOW)
                GPIO.output(gpio_elevator_motor_out_4,GPIO.LOW)
                time.sleep(0.03)
                #time.sleep(1)
            elif i==1:
                GPIO.output(gpio_elevator_motor_out_1,GPIO.HIGH)
                GPIO.output(gpio_elevator_motor_out_2,GPIO.HIGH)
                GPIO.output(gpio_elevator_motor_out_3,GPIO.LOW)
                GPIO.output(gpio_elevator_motor_out_4,GPIO.LOW)
                time.sleep(0.03)
                #time.sleep(1)
            elif i==2:  
                GPIO.output(gpio_elevator_motor_out_1,GPIO.LOW)
                GPIO.output(gpio_elevator_motor_out_2,GPIO.HIGH)
                GPIO.output(gpio_elevator_motor_out_3,GPIO.LOW)
                GPIO.output(gpio_elevator_motor_out_4,GPIO.LOW)
                time.sleep(0.03)
                #time.sleep(1)
            elif i==3:    
                GPIO.output(gpio_elevator_motor_out_1,GPIO.LOW)
                GPIO.output(gpio_elevator_motor_out_2,GPIO.HIGH)
                GPIO.output(gpio_elevator_motor_out_3,GPIO.HIGH)
                GPIO.output(gpio_elevator_motor_out_4,GPIO.LOW)
                time.sleep(0.03)
                #time.sleep(1)
            elif i==4:  
                GPIO.output(gpio_elevator_motor_out_1,GPIO.LOW)
                GPIO.output(gpio_elevator_motor_out_2,GPIO.LOW)
                GPIO.output(gpio_elevator_motor_out_3,GPIO.HIGH)
                GPIO.output(gpio_elevator_motor_out_4,GPIO.LOW)
                time.sleep(0.03)
                #time.sleep(1)
            elif i==5:
                GPIO.output(gpio_elevator_motor_out_1,GPIO.LOW)
                GPIO.output(gpio_elevator_motor_out_2,GPIO.LOW)
                GPIO.output(gpio_elevator_motor_out_3,GPIO.HIGH)
                GPIO.output(gpio_elevator_motor_out_4,GPIO.HIGH)
                time.sleep(0.03)
                #time.sleep(1)
            elif i==6:    
                GPIO.output(gpio_elevator_motor_out_1,GPIO.LOW)
                GPIO.output(gpio_elevator_motor_out_2,GPIO.LOW)
                GPIO.output(gpio_elevator_motor_out_3,GPIO.LOW)
                GPIO.output(gpio_elevator_motor_out_4,GPIO.HIGH)
                time.sleep(0.03)
                #time.sleep(1)
            elif i==7:    
                GPIO.output(gpio_elevator_motor_out_1,GPIO.HIGH)
                GPIO.output(gpio_elevator_motor_out_2,GPIO.LOW)
                GPIO.output(gpio_elevator_motor_out_3,GPIO.LOW)
                GPIO.output(gpio_elevator_motor_out_4,GPIO.HIGH)
                time.sleep(0.03)
                #time.sleep(1)
            if i==7:
                i=0
                continue
            i=i+1
    elif x<0 and x>=-400:
        x=x*-1
        for y in range(x,0,-1):
            if positive==1:
                if i==0:
                    i=7
                else:
                    i=i-1
                y=y+3
                positive=0
            negative=1
            #print((x+1)-y) 
            if i==0:
                GPIO.output(gpio_elevator_motor_out_1,GPIO.HIGH)
                GPIO.output(gpio_elevator_motor_out_2,GPIO.LOW)
                GPIO.output(gpio_elevator_motor_out_3,GPIO.LOW)
                GPIO.output(gpio_elevator_motor_out_4,GPIO.LOW)
                time.sleep(0.03)
                #time.sleep(1)
            elif i==1:
                GPIO.output(gpio_elevator_motor_out_1,GPIO.HIGH)
                GPIO.output(gpio_elevator_motor_out_2,GPIO.HIGH)
                GPIO.output(gpio_elevator_motor_out_3,GPIO.LOW)
                GPIO.output(gpio_elevator_motor_out_4,GPIO.LOW)
                time.sleep(0.03)
                #time.sleep(1)
            elif i==2:  
                GPIO.output(gpio_elevator_motor_out_1,GPIO.LOW)
                GPIO.output(gpio_elevator_motor_out_2,GPIO.HIGH)
                GPIO.output(gpio_elevator_motor_out_3,GPIO.LOW)
                GPIO.output(gpio_elevator_motor_out_4,GPIO.LOW)
                time.sleep(0.03)
                #time.sleep(1)
            elif i==3:    
                GPIO.output(gpio_elevator_motor_out_1,GPIO.LOW)
                GPIO.output(gpio_elevator_motor_out_2,GPIO.HIGH)
                GPIO.output(gpio_elevator_motor_out_3,GPIO.HIGH)
                GPIO.output(gpio_elevator_motor_out_4,GPIO.LOW)
                time.sleep(0.03)
                #time.sleep(1)
            elif i==4:  
                GPIO.output(gpio_elevator_motor_out_1,GPIO.LOW)
                GPIO.output(gpio_elevator_motor_out_2,GPIO.LOW)
                GPIO.output(gpio_elevator_motor_out_3,GPIO.HIGH)
                GPIO.output(gpio_elevator_motor_out_4,GPIO.LOW)
                time.sleep(0.03)
                #time.sleep(1)
            elif i==5:
                GPIO.output(gpio_elevator_motor_out_1,GPIO.LOW)
                GPIO.output(gpio_elevator_motor_out_2,GPIO.LOW)
                GPIO.output(gpio_elevator_motor_out_3,GPIO.HIGH)
                GPIO.output(gpio_elevator_motor_out_4,GPIO.HIGH)
                time.sleep(0.03)
                #time.sleep(1)
            elif i==6:    
                GPIO.output(gpio_elevator_motor_out_1,GPIO.LOW)
                GPIO.output(gpio_elevator_motor_out_2,GPIO.LOW)
                GPIO.output(gpio_elevator_motor_out_3,GPIO.LOW)
                GPIO.output(gpio_elevator_motor_out_4,GPIO.HIGH)
                time.sleep(0.03)
                #time.sleep(1)
            elif i==7:    
                GPIO.output(gpio_elevator_motor_out_1,GPIO.HIGH)
                GPIO.output(gpio_elevator_motor_out_2,GPIO.LOW)
                GPIO.output(gpio_elevator_motor_out_3,GPIO.LOW)
                GPIO.output(gpio_elevator_motor_out_4,GPIO.HIGH)
                time.sleep(0.03)
                #time.sleep(1)
            if i==0:
                i=7
                continue
            i=i-1 
            
def wait_for_action():
    while True:
        if current_state == State.UP:
            x = 1
        elif current_state == State.DOWN:
            x = 1
        elif current_state == State.STATIONARY:
            x = 1
            
        time.sleep(1) 

do_init()
wait_for_action()
do_exit()