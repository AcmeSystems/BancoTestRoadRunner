from time import sleep
import sys
import os
import subprocess

print("Roadrunner text bench 2.1");

testpairs = [ 
	["PA30","PA14"],
	["PC9","PB7"],
	["PC11","PC21"],
	["PC23","PD18"],
	["PD5","PD14"],
	["PD17","PD15"],
	["PD16","PD11"],
	["PD6","PD11"],
	["PD24","PD28"],
	["PB6","PB10"],
	["PD23","PD31"],
	["PC8", "PA7"],
	["PA2", "PA4"],
	["PA26","PA29"],
	["PA3", "PA10"],
	["PA1", "PA23"],
	["PA15","PA27"],
	["PB0", "PA24"],
	["PA31","PA25"],
	["PB31","PB29"],
	["PB27","PB25"],
	["PB30","PB28"],
	["PB26","PB24"],
	["PD25","PD27"],
	["PD26","PC5"],
	["PC7", "PC4"],
	["PC3", "PA5"],
	["PC6", "PA0"],
	["PA9", "PA16"],
	["PA12","PA16"],
	["PC2", "PC1"],
	["PC0", "PA6"],
	["PA8", "PA11"],
	["PA13","PA17"],
	["PB11","PB4"],
	["PB3", "PB2"],
	["PD4", "PC30"],
	["PC15","PC13"],
	["PC19","PC17"],
	["PC27","PC25"],
	["PB13","PB12"],
	["PB5","PB1"],
	["PC31","PC14"],
	["PC12","PC10"],
	["PC20","PC18"],
	["PC16","PC26"],
	["PC24","PC22"],
	["PD19","PD20"],
	["PD21","PD22"],
	["PB8","PB9"],
	["PC28","PC29"],
	["PD1","PD0"],
	["PD12","PD9"],
	["PD13","PD8"],
	["PD10","PD7"],
]

def pin2id(pinname):

	"""
	Return the Kernel ID of any Pin using the MCU name
	or the board name
	"""

	offset=None
	if pinname[0:2]=="PA":
		offset=0
	if pinname[0:2]=="PB":
		offset=32
	if pinname[0:2]=="PC":
		offset=64
	if pinname[0:2]=="PD":
		offset=96

	if offset==None:
		return None
	else:	
		return offset+int(pinname[2:4])

#for pin in testpairs:
#	print(pin2id(pin[0]),pin2id(pin[1]))
 
