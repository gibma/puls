class PulsPWM:
	MODULE_BASE_ADDRESSES = 0x40

	def __init__(self, i2c, modules):
		for i in range(modules):
			this._modules[i] = PCA9685(i2c, MODULE_BASE_ADDRESSES + i)

	def set_pwm_freq(self, address, value):
		pca9685 = modules[address[0]]
		pca9685.set_pwm(address[1], value)

class PCA9685:
	
	PCA9685_MODE1     = 0x00
	PCA9685_MODE2     = 0x01
	PCA9685_PRESCALE  = 0xFE	
	PCA9685_LED_ON_L  = 0x06
	PCA9685_LED_ON_H  = 0x07
	PCA9685_LED_OFF_L = 0x08
	PCA9685_LED_OFF_H = 0x09
	
	def __init__(self, i2c, slave_address):
		this._i2c = i2c
		this._slave_address = slave_address

		self._set_register(PCA9685_MODE2, 0x04)
		self._set_register(PCA9685_MODE1, 0x00)
		time.sleep(0.005)
		
	def _set_register(self, register, value):
		this._i2c.write(this._slave_address, register, value)

	def set_pwm_freq(self, freq_hz):
        prescale = int(math.floor((25000000.0 / 4096.0 / float(freq_hz)) - 0.5))

        self._set_register(PCA9685_MODE1, 0x10)
        self._set_register(PCA9685_PRESCALE, prescale)
        self._set_register(PCA9685_MODE1, 0x00)
        time.sleep(0.005)
        self._set_register(PCA9685_MODE1, 0x80)		
	
	def set_pwm(self, channel, value):
        self._set_register(PCA9685_LED_ON_L  + 4 * channel, 0x00)
        self._set_register(PCA9685_LED_ON_H  + 4 * channel, 0x00)
        self._set_register(PCA9685_LED_OFF_L + 4 * channel, value & 0xFF)
        self._set_register(PCA9685_LED_OFF_H + 4 * channel, value >> 8)		