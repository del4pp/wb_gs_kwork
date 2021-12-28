import pywhatkit
from datetime import datetime

date_now = datetime.now().date()
time_hour = datetime.now().time().hour
time_minute = int(datetime.now().time().minute) + 1

pywhatkit.sendwhatmsg('+380971971716', 'Привіт', time_hour, time_minute)
pywhatkit.sendwhatmsg('+380971971716', 'дюндель', time_hour, time_minute)