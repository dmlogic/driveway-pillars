#!/usr/bin python

import ephem
import time
import datetime
import sys
import RPi.GPIO as GPIO
import config

rightAboutNow = datetime.datetime
boundsTime = rightAboutNow.now().strftime("%H:%M")
timeNow = rightAboutNow.utcnow().strftime("%H:%M")
# timeNow = "05:01"
# boundsTime = timeNow
GPIO.setmode(GPIO.BCM)
GPIO.setup(config.controlPin,GPIO.OUT)

def debug(msg):
    if(not config.debug):
        return
    print(msg)

def turnOn():
    debug("Turn on")
    GPIO.output(config.controlPin,0)
    quit();

def turnOff():
    debug("Turn off")
    GPIO.output(config.controlPin,1)
    quit();

debug("It is now "+ boundsTime)

# If we're out of bounds, turn off and quit
if boundsTime > config.turnOffLate or boundsTime < config.turnOnEarly:
    debug("out of bounds")
    turnOff();

# Make an observer
home = ephem.Observer()
sun = ephem.Sun()

# Remember PyEphem takes and returns only UTC times
home.date = rightAboutNow.utcnow().strftime("%Y-%m-%d %H-%M:00")

# Location of Larkfield Road
home.lat  = str(config.lat)
home.lon  = str(config.lon)
home.elev = config.elev # Because accuracy is important, right?!

sunrise = home.previous_rising(sun).datetime()
sunset = home.next_setting(sun).datetime()
morningTime = sunrise - datetime.timedelta(seconds=config.minutesOffet)
eveningTime = sunset + datetime.timedelta(seconds=config.minutesOffet)
morningTurnOff = morningTime.strftime("%H:%M")
eveningTurnOn = eveningTime.strftime("%H:%M")

debug("UTC time is "+timeNow)
debug("Sunrise today is at "+morningTurnOff)
debug("Sunset today is at "+eveningTurnOn)

# Turn on conditions:
#   sunrise is later than turn on time AND it is earlier than sunrise time
#   OR
#   sunset is  earlier than turn off time AND it is later than sunset time

if (morningTurnOff > config.turnOnEarly and timeNow > config.turnOnEarly and timeNow < morningTurnOff) or (eveningTurnOn < config.turnOffLate and timeNow >= eveningTurnOn and timeNow < config.turnOffLate):
    turnOn();

# Turn off conditions
#   sunrise is earlier than now or sunset is earlier than now
#   OR
#   it is later than turnoff

if (morningTurnOff < timeNow or eveningTurnOn > timeNow) or (timeNow > turnOffLate):
    turnOff();

debug("No match :(")
