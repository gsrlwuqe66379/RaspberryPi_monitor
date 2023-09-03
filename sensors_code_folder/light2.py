#!/usr/bin/env python
import PCF8591 as ADC
import RPi.GPIO as GPIO
import time
DO = 17
GPIO.setmode(GPIO.BCM)

def setup():
	ADC.setup(0x48)
	GPIO.setup(DO, GPIO.IN)


def loop():
	status = 1
	while True:
		print ('#######################')
		print ('Digital output: ',GPIO.input(DO) ) #光强输出低电平，光弱输出高电平
		print ('#######################')
		time.sleep(0.5)

if __name__ == '__main__':
	try:
		setup()
		loop()
	except KeyboardInterrupt: 
		pass	


