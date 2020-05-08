from trrlib import testpairs
from trrlib import pin2id

from mpio import GPIO
from mpio import DevMem

from time import sleep
import sys
import os
import subprocess

print("RoadRunner text bench 2.1")

# Da PD14 a PD18 sono liberi ma con pull-down
# PA30 libero ma con un pull-down

# read the CHIP ID register on SAMA5D2
print "0x{0:04x}".format(DevMem.read_reg(0xFC069000))

# pag 459 datasheet SAMA5D2 for configuration registers
# segnali PD14 .. PD18 sono assegnati con fuse a Periph A (JTAG)
# per assegnarli a GPIO senza riprogrammare i fusibili:
# mem2io -w -i fc0380c0,7c000
# mem2io -w -i fc0380c4,200

DevMem.write_reg(0xfc0380c0,0x7c000)
DevMem.write_reg(0xfc0380c4,0x00200)

gpio = GPIO(pin2id("PD14"), GPIO.IN)
print gpio.get()

gpio = GPIO(pin2id("PD15"), GPIO.IN)
print gpio.get()

gpio = GPIO(pin2id("PD16"), GPIO.IN)
print gpio.get()

gpio = GPIO(pin2id("PD17"), GPIO.IN)
print gpio.get()

gpio = GPIO(pin2id("PD17"), GPIO.IN)
print gpio.get()

gpio = GPIO(pin2id("PA30"), GPIO.IN)
print gpio.get()
