# IMPORTS
from time import sleep
from gpiozero import RGBLED
from colorzero import Color
from Logger import Logger
from PiPadConfiguration import led as _conf

# LOGGER
log = Logger(_conf['DEVEL_LOG'])

# PiPAD LED
class PiPadLED :

    # initialize
    def __init__(self) :

        # set PINs on BOARD
        log.debug("Initializing LEDs...")
        log.debug("> RED pin: " + str(_conf['red_pin']))
        log.debug("> GREEN pin: " + str(_conf['green_pin']))
        log.debug("> BLUE pin: " + str(_conf['blue_pin']))
        self.rgbled = RGBLED(_conf['red_pin'], _conf['green_pin'], _conf['blue_pin'])
        log.debug("...init done!")

    # off
    def off(self) :
        log.debug("Set to off")
        self.rgbled.off()

    # on
    def on(self) :
        log.debug("Set to on")
        self.color()

    # set color
    def color(self, color = "white", time = 0) :
        log.debug("Set to " + color + " color for " + str(time) + "s")
        self.rgbled.color = Color(color)
        if not time == 0 :
            sleep(time)
            self.rgbled.off()

    # terminate
    def terminate(self) :
        log.debug("LEDs termination...")
        self.rgbled.close()

# DEBUG
if __name__ == "__main__":

    log.log("Welcome! Testing LED:")
    time = _conf['led_wait_time']
    led = PiPadLED()
    try :

        log.log("White...")
        led.color("white", time)

        log.log("Magenta...")
        led.color("magenta", time)

        log.log("Cyan...")
        led.color("cyan", time)

        log.log("Yellow...")
        led.color("yellow", time)

        log.log("Blue...")
        led.color("blue", time)

        log.log("Green...")
        led.color("green", time)

        log.log("Red...")
        led.color("red", time)

        led.off()
    
    # capture interruption
    except KeyboardInterrupt:
        pass
    
    led.terminate()
    del led
    log.log("Goodbye!")
