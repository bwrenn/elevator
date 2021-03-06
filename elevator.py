import RPi.GPIO as GPIO
import time
from gpiozero import Button
from enum import Enum
import sys
#from __builtin__ import True

class State(Enum):
    DOWN = 0
    UP = 1
    STATIONARY = 3
    
class Light(Enum):
    GOING_DOWN_PRESSED = 0
    GOING_DOWN_ARRIVED = 1
    GOING_UP_PRESSED = 2
    GOING_UP_ARRIVED = 3
    
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

stop_at_floor_up = [ False, False, False ]
stop_at_floor_dn = [ False, False, False ]

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
   
    global stop_at_floor_up
    global stop_at_floor_dn
    stop_at_floor_up = [ False, False, False ]
    stop_at_floor_dn = [ False, False, False ]
    
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
    stop_at_floor_up[floor_1] = True
    illuminate(floor_1, Light.GOING_UP_PRESSED)

def button_floor_2_dn_pressed():
    print("2 down pressed")
    stop_at_floor_dn[floor_2] = True
    illuminate(floor_2, Light.GOING_DOWN_PRESSED)

def button_floor_2_up_pressed():
    print("2 up pressed")
    stop_at_floor_up[floor_2] = True
    illuminate(floor_2, Light.GOING_UP_PRESSED)

def button_floor_3_dn_pressed():
    print("3 down pressed")
    stop_at_floor_dn[floor_3] = True
    illuminate(floor_3, Light.GOING_DOWN_PRESSED)
    
def illuminate(floor, light):
    if floor_1 == floor:
        if light == Light.GOING_UP_ARRIVED:
            GPIO.output(gpio_led_floor_1_up_arrived, GPIO.HIGH)
        elif light == Light.GOING_UP_PRESSED:
            GPIO.output(gpio_led_floor_1_up_pressed, GPIO.HIGH)
    elif floor_2 == floor:
        if light == Light.GOING_DOWN_ARRIVED:
            GPIO.output(gpio_led_floor_2_dn_arrived, GPIO.HIGH)
        elif light == Light.GOING_DOWN_PRESSED:
            GPIO.output(gpio_led_floor_2_dn_pressed, GPIO.HIGH)
        elif light == Light.GOING_UP_ARRIVED:
            GPIO.output(gpio_led_floor_2_up_arrived, GPIO.HIGH)
        elif light == Light.GOING_UP_PRESSED:
            GPIO.output(gpio_led_floor_2_up_pressed, GPIO.HIGH)
    if floor_3 == floor:
        if light == Light.GOING_DOWN_ARRIVED:
            GPIO.output(gpio_led_floor_3_dn_arrived, GPIO.HIGH)
        elif light == Light.GOING_DOWN_PRESSED:
            GPIO.output(gpio_led_floor_3_dn_pressed, GPIO.HIGH)
    
def un_illuminate(floor, light):
    if floor_1 == floor:
        if light == Light.GOING_UP_ARRIVED or light == Light.GOING_DOWN_ARRIVED:
            GPIO.output(gpio_led_floor_1_up_arrived, GPIO.LOW)
        elif light == Light.GOING_UP_PRESSED or light == Light.GOING_DOWN_PRESSED:
            GPIO.output(gpio_led_floor_1_up_pressed, GPIO.LOW)
    elif floor_2 == floor:
        if light == Light.GOING_DOWN_ARRIVED:
            GPIO.output(gpio_led_floor_2_dn_arrived, GPIO.LOW)
        elif light == Light.GOING_DOWN_PRESSED:
            GPIO.output(gpio_led_floor_2_dn_pressed, GPIO.LOW)
        elif light == Light.GOING_UP_ARRIVED:
            GPIO.output(gpio_led_floor_2_up_arrived, GPIO.LOW)
        elif light == Light.GOING_UP_PRESSED:
            GPIO.output(gpio_led_floor_2_up_pressed, GPIO.LOW)
    if floor_3 == floor:
        if light == Light.GOING_DOWN_ARRIVED or light == Light.GOING_UP_ARRIVED:
            GPIO.output(gpio_led_floor_3_dn_arrived, GPIO.LOW)
        elif light == Light.GOING_DOWN_PRESSED or light == Light.GOING_UP_PRESSED:
            GPIO.output(gpio_led_floor_3_dn_pressed, GPIO.LOW)

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

def get_next_state():
    global current_floor
    global current_state
    
    if current_floor == floor_1:
        if stop_at_floor_up[floor_2] or stop_at_floor_dn[floor_2] or stop_at_floor_dn[floor_3]:
            return State.UP
        else:
            return State.STATIONARY
    if current_floor == floor_2:
        if current_state == State.UP:
            if stop_at_floor_dn[floor_3]:
                return State.UP
            elif stop_at_floor_up[floor_1]:
                return State.DOWN
            else:
                return State.STATIONARY
        elif current_state == State.DOWN:
            if stop_at_floor_up[floor_1]:
                return State.DOWN
            elif stop_at_floor_dn[floor_3]:
                return State.UP
            else:
                return State.STATIONARY
        elif current_state == State.STATIONARY:
            if stop_at_floor_up[floor_1]:
                return State.DOWN
            elif stop_at_floor_dn[floor_3]:
                return State.UP
            else:
                return State.STATIONARY
    if current_floor == floor_3:
        if stop_at_floor_dn[floor_2] or stop_at_floor_up[floor_2] or stop_at_floor_up[floor_1]:
            return State.DOWN
        else:
            return State.STATIONARY

def go_down():
    global current_floor
    global current_state
    
    print("going down from floor " + str(current_floor + 1))
    if current_floor > floor_1:
        current_floor = current_floor - 1
    if floor_1 == current_floor or stop_at_floor_dn[current_floor] == True:
        service_current_floor()
        
def go_up():
    global current_floor
    global current_state
    
    print("going up from floor " + str(current_floor + 1))
    if current_floor < floor_3:
        current_floor = current_floor + 1
    if floor_3 == current_floor or stop_at_floor_up[current_floor] == True:
        service_current_floor()
        
def service_current_floor():
    global current_floor
    global current_state
    
    print("service floor " + str(current_floor + 1))
    
    if current_floor == floor_1:
        stop_at_floor_up[current_floor] = False
        illuminate(current_floor, Light.GOING_UP_ARRIVED)
        un_illuminate(current_floor, Light.GOING_UP_PRESSED)
    elif current_floor == floor_2:
        if current_state == State.DOWN and stop_at_floor_dn[floor_2]:
            stop_at_floor_dn[current_floor] = False
            illuminate(current_floor, Light.GOING_DOWN_ARRIVED)
            un_illuminate(current_floor, Light.GOING_DOWN_PRESSED)
        elif current_state == State.UP and stop_at_floor_up[floor_2]:
            stop_at_floor_up[current_floor] = False
            illuminate(current_floor, Light.GOING_UP_ARRIVED)
            un_illuminate(current_floor, Light.GOING_UP_PRESSED)
        elif current_state == State.STATIONARY:
            if stop_at_floor_up[floor_2]:
                stop_at_floor_up[current_floor] = False
                illuminate(current_floor, Light.GOING_UP_ARRIVED)
                un_illuminate(current_floor, Light.GOING_UP_PRESSED)
            elif stop_at_floor_dn[floor_2]:
                stop_at_floor_dn[current_floor] = False
                illuminate(current_floor, Light.GOING_DOWN_ARRIVED)
                un_illuminate(current_floor, Light.GOING_DOWN_PRESSED)
    elif current_floor == floor_3:
        stop_at_floor_dn[floor_3] = False
        illuminate(current_floor, Light.GOING_DOWN_ARRIVED)
        un_illuminate(current_floor, Light.GOING_DOWN_PRESSED)
        
    print("done servicing floor")
   
def leave_current_floor(clear_floor): 
    global current_floor
    global current_state
    
    print("leave floor " + str(current_floor + 1))
    if current_floor == floor_1:
        un_illuminate(current_floor, Light.GOING_UP_ARRIVED)
        stop_at_floor_up[floor_1] = False
    elif current_floor == floor_2:
        if current_state == State.DOWN:# and stop_at_floor_dn[floor_2]:
            print("@@@ here-1")
            un_illuminate(current_floor, Light.GOING_DOWN_ARRIVED)
        elif current_state == State.UP:# and stop_at_floor_up[floor_2]:
            print("@@@ here-2")
            un_illuminate(current_floor, Light.GOING_UP_ARRIVED)
    elif current_floor == floor_3:
        un_illuminate(current_floor, Light.GOING_DOWN_ARRIVED)
        
    if clear_floor:
        un_illuminate(current_floor, Light.GOING_DOWN_ARRIVED)
        un_illuminate(current_floor, Light.GOING_UP_ARRIVED)
        stop_at_floor_dn[current_floor] = False
        stop_at_floor_up[current_floor] = False
    
def wait_for_action():
    while True:
        global current_state
        
        previous_state = current_state 
        current_state = get_next_state()
       
        if current_state != State.STATIONARY:
            leave_current_floor(State.STATIONARY == previous_state)
        
        if current_state == State.DOWN:
            go_down()
        elif current_state == State.UP:
            go_up()
        elif current_state == State.STATIONARY:
            service_current_floor()
        
        print("current floor: " + str(current_floor + 1))
        print("current state: " + str(current_state))
        print("pressed down: [" + str(stop_at_floor_dn[floor_1]) + "," +
            str(stop_at_floor_dn[floor_2]) + "," + str(stop_at_floor_dn[floor_3]) + "]")
        print("pressed up: [" + str(stop_at_floor_up[floor_1]) + "," +
            str(stop_at_floor_up[floor_2]) + "," + str(stop_at_floor_up[floor_3]) + "]")
       
        print("") 
        print("--------------------------------------------------------------")
        print("Ready...")
        data = sys.stdin.readline()

do_init()
wait_for_action()
do_exit()