#import RPi.GPIO as GPIO

RELAY_PINS = [1,2,3,4,5,6,7,8,9]

class PulsGPIO:

	def __init__(self):
		#GPIO.setmode(GPIO.BOARD)
		#GPIO.setup(RELAY_PINS, GPIO.OUT)			
		pass
		
	def set_pwm(self, address, value):
		print("PWM", address, value)
		
	def set_relay(self, address, value):
		pin = RELAY_PINS[address]
		#GPIO.output(pin, value)
		
	def close(self):
		#GPIO.cleanup()
		pass