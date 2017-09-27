import RPi.GPIO as GPIO

RELAY_PINS = [[1,2,3,4],[5,6,7,8],[9,10,11,12]]

class PulsRelay:

	def __init__(self):
		GPIO.setmode(GPIO.BOARD)
		GPIO.setup(RELAY_PINS, GPIO.OUT)			
		pass
	
	def set_relay(self, address, value):
		pin = RELAY_PINS[address[0]][address[1]]
		GPIO.output(pin, value)
		
	def close(self):
		GPIO.cleanup()
		pass