from mpio import GPIO
from trrlib import pin2id
from time import sleep

gpio = GPIO(pin2id("PA30"), GPIO.IN)
print gpio.get()
