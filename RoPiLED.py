# IMPORTS
from gpiozero import RGBLED
from gpiozero.pins.pigpio import PiGPIOFactory
from colorzero import Color
from time import sleep
from Logger import Logger
from RoPiConfiguration import led as _conf

# LOGGER
log = Logger(_conf['DEVEL_LOG'])

# ROPI LED!
class RoPiLED :

    # initialize
    def __init__(self, remote_address) :

        # set PINs on BOARD
        log.debug("Initializing LEDs...")
        log.debug("> RED: " + str(_conf['red_pin']))
        log.debug("> GREEN: " + str(_conf['green_pin']))
        log.debug("> BLUE: " + str(_conf['blue_pin']))

        # using RGBLED
        rem_pi = PiGPIOFactory(host=remote_address)
        self.rgbled = RGBLED(red=_conf['red_pin'], green=_conf['green_pin'], blue=_conf['blue_pin'], pin_factory=rem_pi)
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
    def color(self, color = "white", time = 0, off = False) :
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
    led = RoPiLED("192.168.1.118")
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
