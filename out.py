from mpio import GPIO
from trrlib import pin2id
from time import sleep

gpio = GPIO(pin2id("PA17"), GPIO.OUT)
gpio.set(True)
sleep(1)   
gpio.set(False)
