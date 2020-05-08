import mpio
import time
from trrlib import testpairs
from trrlib import pin2id

counter=0
for pin in testpairs:
	test=True;
	
	gpio_out = mpio.GPIO(pin2id(pin[0]), mpio.GPIO.OUT)
	gpio_inp = mpio.GPIO(pin2id(pin[1]), mpio.GPIO.IN)

	gpio_out.set(True)
	if gpio_inp.get()!=True:
		test=False
		
	gpio_out.set(False)
	if gpio_inp.get()!=False:
		test=False

	gpio_out = mpio.GPIO(pin2id(pin[1]), mpio.GPIO.OUT)
	gpio_inp = mpio.GPIO(pin2id(pin[0]), mpio.GPIO.IN)

	gpio_out.set(True)
	if gpio_inp.get()!=True:
		test=False
		
	gpio_out.set(False)
	if gpio_inp.get()!=False:
		test=False

	if test==False:
		state_description="--> KO";
	else:
		state_description="-";
	
	counter+=1	
	print(counter,pin[0],pin[1],test)

