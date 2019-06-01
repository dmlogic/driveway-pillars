# driveway-pillars

Sync lighting control to sunset / sunrise

Turns on relay to power lights x minutes after sunset until shutoff and from startup until x minutes before sunrise.

Requires:

* A Raspi with `RPi.GPIO`
* [pyephem](http://rhodesmill.org/pyephem/)
