from trrlib import testlistpullup
from trrlib import pin2id

import mpio

from time import sleep
import sys
import os
import subprocess

print("RoadRunner text bench 2.1")

# Pag 459 datasheet SAMA5D2 for configuration registers
# segnali PD14 .. PD18 sono assegnati con fuse a Periph A (JTAG)
# per assegnarli a GPIO senza riprogrammare i fusibili:
# mem2io -w -i fc0380c0,7c000
# mem2io -w -i fc0380c4,200

mpio.DevMem.write_reg(0xfc0380c0,0x0007c000)
mpio.DevMem.write_reg(0xfc0380c4,0x00000200)

# Put PA30 as normal gpio with pullup
# os.system("mem2io -w -i fc038000,40000000")
# os.system("mem2io -w -i fc038004,200")

mpio.DevMem.write_reg(0xfc038000,0x40000000)
mpio.DevMem.write_reg(0xfc038004,0x00000200)

color_warning = "\x1B[30;41m"
color_pass = "\x1B[30;42m"
color_normal = "\x1B[0m"
color_check = "\x1B[31m" 

numerrors = 0
step = 0

"""
#***********************************************************************
# Test ADC
#***********************************************************************
os.system("cp /sys/bus/iio/devices/iio\:device0/in_voltage10_raw ad10")
adc10 = subprocess.check_output(["cat", "ad10"])
test = [int(s) for s in adc10.split() if s.isdigit()][0]  #estrae il numero
#print "adc10 = %s" % test
if test<1200 or test>2000:
	print (color_warning + "Error AD10! %s (1200..2000)" + color_normal) % (test)
	numerrors = numerrors+1
else:
	print (color_pass + "AD10 OK! %s (1200..2000)" + color_normal) % (test)
	
os.system("cp /sys/bus/iio/devices/iio\:device0/in_voltage11_raw ad11")
adc11 = subprocess.check_output(["cat", "ad11"])
test = [int(s) for s in adc11.split() if s.isdigit()][0]  #estrae il numero
#print "adc11 = %s" % test
if test<420 or test>1220:
	print (color_warning + "Error AD11! %s (420..1220)" + color_normal) % (test)
	numerrors = numerrors+1
else:
	print (color_pass + "AD11 OK! %s (420..1220)" + color_normal) % (test)
"""

#***********************************************************************
# Test GPIO
#***********************************************************************

print "Test GPIO"

# Ciclo di scansione e test dei GPIO

myIN = False

error_counter=0

for test in testlistpullup:
	testpinOUT = mpio.GPIO(pin2id(test[0]), mpio.GPIO.OUT)
	testpinIN = mpio.GPIO(pin2id(test[1]), mpio.GPIO.IN)

	testpinOUT.set(True)

#	sleep(0.05)
	myIN = testpinIN.get()
	if step > 0:
		print "%s -> %s" % (test[0],test[1])
		print "test0=1 -> test1=%s " % myIN 

	if myIN==False:
		print (color_warning + "%s=1 --> %s==1 ?" + color_normal) % (test[0],test[1]),
		print (color_warning + "Errore ! %s in corto verso massa" + color_normal) % (test[1])
		error_counter = error_counter + 1
		if step > 0:
			raw_input(" Press Enter")
	if step > 1:
		raw_input(" Press Enter")

	testpinOUT.set(False)
#	sleep(0.05)
	myIN = testpinIN.get()

	if step > 0:
		print "test0=0 -> test1=%s " % myIN 

	if myIN==False:
		print (color_warning + "%s=0 --> %s==1 ? " + color_normal) % (test[0],test[1]),
		print (color_warning + "Errore ! Corto tra %s e %s" + color_normal) % (test[0],test[1])
		error_counter = error_counter + 1
		if step > 0:
			raw_input(" Press Enter")
	if step > 1:
		raw_input(" Press Enter")

	testpinOUT = mpio.GPIO(pin2id(test[1]),mpio.GPIO.OUT)
	testpinIN = mpio.GPIO(pin2id(test[0]), mpio.GPIO.IN)
	testpinOUT.set(True)

#	sleep(0.05)

	myIN = testpinIN.get()
	if step > 0:
		print "test1=1 -> test0=%s " % myIN 

	if myIN==False:
		print (color_warning + "%s==1 ? <-- %s=1" + color_normal) % (test[0],test[1]),
		print (color_warning + "Error ! %s in corto verso massa" + color_normal) % (test[0])
		error_counter = error_counter + 1
		if step > 0:
			raw_input(" Press Enter")
	if step > 1:
		raw_input(" Press Enter")

	testpinOUT.set(False)
#	sleep(0.05)
	myIN = testpinIN.get()
	if step > 0:
		print "test1=0 -> test0=%s " % myIN 

	if myIN==True:
		print (color_warning + "%s==0 ? <-- %s=0 " + color_normal) % (test[0],test[1]),
		print (color_warning + "Errore ! %s o %s a circuito aperto oppure %s a 3.3v" + color_normal) % (test[0],test[1],test[0])
		error_counter = error_counter + 1
		if step > 0:
			raw_input(" Press Enter")
	if step > 1:
		raw_input(" Press Enter")

	testpinOUT = mpio.GPIO(pin2id(test[0]), mpio.GPIO.OUT)
	testpinIN = mpio.GPIO(pin2id(test[1]), mpio.GPIO.IN)
#	sleep(0.05)

if error_counter==0:
	print color_pass + "GPIO pullup test OK" + color_normal
else:
	print (color_warning + "Errors pullup: %d" + color_normal) % error_counter
	numerrors = numerrors + 1
sleep(0.1)

#error_counter = 0


#print "fine test gpio : while True ..."

#while True:
#	sleep(1)

sleep(0.1)
os.system("date")
sleep(1.0)

"""
#***********************************************************************
# Test USB
#***********************************************************************
#os.system("dmesg") 
os.system("ls /dev | grep 'ttyUSB0' > testusb")
testusb = subprocess.check_output(["cat", "testusb"])
print "testusb = %s" % (testusb)
if (testusb != ""):
	print color_pass + "USB OK" + color_normal
else:
	numerrors = numerrors + 1
	print (color_warning + "USB ERROR" + color_normal) 

#os.system("dmesg | grep 'CDC' > testusb")
#testusb = subprocess.check_output(["cat", "testusb"])
#print "testusb = %s" % (testusb)
#if (testusb != ""):
#	print color_pass + "USB CDC Gadget OK" + color_normal
#else:
#	numerrors = numerrors + 1
#	print (color_warning + "USB CDC GADGET ERROR" + color_normal) 
"""

"""
#***********************************************************************
# Test RAM
#***********************************************************************

print "Test RAM"


print "DDR2 RAM Test"
if os.system("memtester 10k 1 > null")==0:
	print color_pass + "Memory OK" + color_normal
else:
	print color_warning + "Memory ERROR !" + color_normal
	numerrors = numerrors + 1

print ""
"""

"""
#***********************************************************************
# Test Ethernet
#***********************************************************************

print "Test Ethernet"


if os.system("ping -c 2 192.168.16.1")==0:
	print color_pass + "ETH test OK" + color_normal
	error_eth = 0
else:
	print color_warning + "ERRORE DI RETE" + color_normal
	numerrors = numerrors+1
	error_eth = 1
"""

"""
#***********************************************************************
# Test Mantenimento data      
#***********************************************************************

if (numerrors == 0):
	print "Test Mantenimento data"
	if os.system("date -s '04/13/2020 09:30:00'")==0:
		print color_pass + "Date set OK" + color_normal
		error_eth = 0                                
	else:
		print color_warning + "Date set NOK" + color_normal
		numerrors = numerrors+1
	if os.system("hwclock -w")==0:
		print color_pass + "hwclock OK" + color_normal
	else:
		print color_warning + "hwclock NOK" + color_normal
		numerrors = numerrors+1
	os.system("date") 
	os.system("echo `date '+%s' -d '+ 9 seconds'` > /sys/class/rtc/rtc0/wakealarm")	
	os.system("shutdown -h now")
print "fine test."
"""
