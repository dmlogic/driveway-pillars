#!/usr/bin python

import ephem
import time
import datetime
import sys
import RPi.GPIO as GPIO

rightAboutNow = datetime.datetime
boundsTime = rightAboutNow.now().strftime("%H:%M")
timeNow = rightAboutNow.utcnow().strftime("%H:%M")
turnOnEarly = "05:00"
turnOffLate = "23:00"
controlPin = 16

# timeNow = "19:00"
# boundsTime = timeNow
GPIO.setmode(GPIO.BCM)
GPIO.setup(controlPin,GPIO.OUT)

def turnOn():
    print "Turn on"
    GPIO.output(controlPin,0)
    quit();

def turnOff():
    print "Turn off"
    GPIO.output(controlPin,1)
    quit();

print "It is now ", boundsTime

# If we're out of bounds, turn off and quit
if boundsTime > turnOffLate or boundsTime < turnOnEarly:
    print "out of bounds"
    turnOff();

# Make an observer
home = ephem.Observer()
sun = ephem.Sun()

# Remember PyEphem takes and returns only UTC times
home.date = rightAboutNow.utcnow().strftime("%Y-%m-%d %H-%M:00")

# Location of Larkfield Road
home.lat  = str(SET ME)
home.lon  = str(SET ME)
home.elev = 108 # Because accuracy is important, right?!

sunrise = home.previous_rising(sun).datetime()
sunset = home.next_setting(sun).datetime()

sunriseTime = sunrise.strftime("%H:%M")
sunsetTime = sunset.strftime("%H:%M")

print "UTC time is ",timeNow
print "Sunrise today is at ",sunriseTime
print "Sunset today is at ",sunsetTime

# Turn on conditions:
#   sunrise is later than turn on time AND it is earlier than sunrise time
#   OR
#   sunset is  earlier than turn off time AND it is later than sunset time

if (sunriseTime > turnOnEarly and timeNow > turnOnEarly and timeNow < sunriseTime) or (sunsetTime < turnOffLate and timeNow >= sunsetTime and timeNow < turnOffLate):
    turnOn();

# Turn off conditions
#   sunrise is earlier than now or sunset is earlier than now
#   OR
#   it is later than turnoff

if (sunriseTime < timeNow or sunsetTime > timeNow) or (timeNow > turnOffLate):
    turnOff();

print "No match :("
