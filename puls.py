from puls_web import PulsWeb
from puls_db import PulsDB
from puls_thread import PulsThread
from puls_gpio import PulsGPIO

gpio = PulsGPIO()
database = PulsDB()
web = PulsWeb(database, "Herrenhaus")
thread = PulsThread(database, gpio)


thread.start()
web.start()

#Blocked until Ctrl-C or Runtime Error

thread.end()
database.end()