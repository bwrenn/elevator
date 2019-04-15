import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

floor_1_pressed = 24
floor_1_arrived = 23
floor_2_pressed = 10
floor_2_arrived = 8
floor_3_pressed = 11
floor_3_arrived = 9
floor_4_pressed = 25
floor_4_arrived = 7


GPIO.setup(floor_1_pressed, GPIO.OUT)
GPIO.setup(floor_1_arrived, GPIO.OUT)
GPIO.setup(floor_2_pressed, GPIO.OUT)
GPIO.setup(floor_2_arrived, GPIO.OUT)
GPIO.setup(floor_3_pressed, GPIO.OUT)
GPIO.setup(floor_3_arrived, GPIO.OUT)
GPIO.setup(floor_4_pressed, GPIO.OUT)
GPIO.setup(floor_4_arrived, GPIO.OUT)

while True:
    GPIO.output(floor_1_pressed, GPIO.HIGH)
    GPIO.output(floor_1_arrived, GPIO.HIGH)
    GPIO.output(floor_2_pressed, GPIO.HIGH)
    GPIO.output(floor_2_arrived, GPIO.HIGH)
    GPIO.output(floor_3_pressed, GPIO.HIGH)
    GPIO.output(floor_3_arrived, GPIO.HIGH)
    GPIO.output(floor_4_pressed, GPIO.HIGH)
    GPIO.output(floor_4_arrived, GPIO.HIGH)
    time.sleep(1)
    GPIO.output(floor_1_pressed, GPIO.LOW)
    GPIO.output(floor_1_arrived, GPIO.LOW)
    GPIO.output(floor_2_pressed, GPIO.LOW)
    GPIO.output(floor_2_arrived, GPIO.LOW)
    GPIO.output(floor_3_pressed, GPIO.LOW)
    GPIO.output(floor_3_arrived, GPIO.LOW)
    GPIO.output(floor_4_pressed, GPIO.LOW)
    GPIO.output(floor_4_arrived, GPIO.LOW)
    time.sleep(1)
