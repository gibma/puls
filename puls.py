from puls_web import PulsWeb
from puls_db import PulsDB
from puls_thread import PulsThread
from puls_relay import PulsRelay
from puls_pwm import PulsPWM
from puls_i2c import I2C

i2c = I2C('/dev/i2c-1')

pwm = PulsPWM(i2c, 6)
relay = PulsRelay()
database = PulsDB()
web = PulsWeb(database, "Herrenhaus")
thread = PulsThread(database, pwm, relay)


thread.start()
web.start()

#Blocked until Ctrl-C or Runtime Error

thread.end()
database.end()