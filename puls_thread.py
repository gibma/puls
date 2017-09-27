from threading import Thread
from time import sleep

SLEEP_TIME = 0.01
PRESCALER = 0.5 / SLEEP_TIME

class PulsThread(Thread):

	def __init__(self, puls_db, puls_pwm, puls_relay):
		Thread.__init__(self)
		self._db = puls_db
		self._pwm = puls_pwm
		self._relay = puls_relay
		
		self._pwm_steps = {}
		self._current_pwm_values = self._db.get_initial_pwm_values()
		self._current_relay_values = self._db.get_initial_relay_values()
		
		self._desired_pwm_values = self._db.get_desired_pwm_values()
		self._desired_relay_values = self._db.get_desired_relay_values()
		self._calculate_pwm_steps();
		
		self.running = True
		
	def run(self):
		while self.running:
			sleep(SLEEP_TIME)
			
			if (self._db.dirty):
				self._desired_pwm_values = self._db.get_desired_pwm_values()
				self._desired_relay_values = self._db.get_desired_relay_values()
				self._calculate_pwm_steps();
				
			for pwm_address in self._current_pwm_values:
				current_pwm_value = self._current_pwm_values[pwm_address]
				desired_pwm_value = self._desired_pwm_values[pwm_address]
				
				if current_pwm_value != desired_pwm_value:
					step = self._pwm_steps[pwm_address]
					new_pwm_value = min(current_pwm_value + step, desired_pwm_value) if current_pwm_value < desired_pwm_value else max(current_pwm_value - step, desired_pwm_value)
					self._pwm.set_pwm(pwm_address, new_pwm_value)
					self._current_pwm_values[pwm_address] = new_pwm_value
			
			for relay_address in self._current_relay_values:
				current_relay_value = self._current_relay_values[relay_address]
				desired_relay_value = self._desired_relay_values[relay_address]
				
				if current_relay_value != desired_relay_value:
					self._relay.set_relay(relay_address, desired_relay_value)
					self._current_relay_values[relay_address] = desired_relay_value
					
	def end(self):
		self.running = False
		self.join()
		
	def _calculate_pwm_steps(self):
		for pwm_address in self._current_pwm_values:
			current_pwm_value = self._current_pwm_values[pwm_address]
			desired_pwm_value = self._desired_pwm_values[pwm_address]
				
			if current_pwm_value != desired_pwm_value:
				pwm_step = round(abs(current_pwm_value - desired_pwm_value) / PRESCALER)
				self._pwm_steps[pwm_address] = pwm_step
	