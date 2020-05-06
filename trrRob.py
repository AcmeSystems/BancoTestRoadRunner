from time import sleep
import acmepins

import sys
import os
import subprocess

print "test roadrunner 2.0"

# aggiungere test uscita caratteri da porta seriale PD3 (UTXD1) e ingresso su PD2 (URXD1) e Bu_RxD.
# aggiungere ADC in DTS e test PD29 (AD10) e PD30 (AD11)

# pag 459 datasheet SAMA5D2 for configuration registers
# segnali PD14 .. PD18 sono assegnati con fuse a Periph A (JTAG)
# per assegnarli a GPIO senza riprogrammare i fusibili:
# mem2io -w -i fc0380c0,7c000
# mem2io -w -i fc0380c4,200
# PA30 e' settato 0x405 cioe' pull down e peripheral E cioe' SDMMC1_CD
## provo a metterlo come GPIO con: mem2io -w -i fc038000,40000000 e mem2io -w -i fc038004,200

# put PD14..PD18 as normal gpios with pullup
os.system("mem2io -w -i fc0380c0,7c000")
os.system("mem2io -w -i fc0380c4,200")

# put PA30 as normal gpio with pullup
os.system("mem2io -w -i fc038000,40000000")
os.system("mem2io -w -i fc038004,200")

color_warning = "\x1B[30;41m"
color_pass = "\x1B[30;42m"
color_normal = "\x1B[0m"
color_check = "\x1B[31m" 

numerrors = 0
step = 0
  

#print "This is the name of the script: ", sys.argv[0]
#print "Number of arguments: ", len(sys.argv)
#print "The arguments are: " , str(sys.argv)

#Roadrunner example
#led = acmepins.GPIO(sys.argv[1],'OUTPUT') 

if False:
	while True:
		led.on()
		print "ON"
		sleep(3)
		led.off()
		print "OFF"
		sleep(3)

testlistpullup = [ 
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



#***********************************************************************
# Test GPIO
#***********************************************************************


print "Test GPIO"

# Ciclo di scansione e test dei GPIO


myIN = False

error_counter=0

for test in testlistpullup:
	testpinOUT = acmepins.GPIO(test[0],'OUTPUT')
	testpinIN = acmepins.GPIO(test[1], 'INPUT')
	testpinOUT.on()
#	sleep(0.05)
	myIN = testpinIN.get_value()
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

	testpinOUT.off()
#	sleep(0.05)
	myIN = testpinIN.get_value()

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

	testpinOUT = acmepins.GPIO(test[1],'OUTPUT')
	testpinIN = acmepins.GPIO(test[0], 'INPUT')
	testpinOUT.on()
#	sleep(0.05)
	myIN = testpinIN.get_value()
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

	testpinOUT.off()
#	sleep(0.05)
	myIN = testpinIN.get_value()
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

	testpinOUT = acmepins.GPIO(test[0], 'INPUT')
	testpinIN = acmepins.GPIO(test[1], 'INPUT')
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

