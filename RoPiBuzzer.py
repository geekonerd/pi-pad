# IMPORTS
from gpiozero import Buzzer
from gpiozero.pins.pigpio import PiGPIOFactory
from time import sleep
from Logger import Logger
from RoPiConfiguration import buzzer as _conf

# LOGGER
log = Logger(_conf['DEVEL_LOG'])

# ROPI BUZZER!
class RoPiBuzzer :

    # initialize
    def __init__(self,  remote_address) :

        # set PINs on BOARD
        log.debug("Initializing Buzzer...")
        log.debug("> buzzer pin: " + str(_conf['buzzer_pin']))

        # using Buzzer
        rem_pi = PiGPIOFactory(host=remote_address)
        self.buzzer = Buzzer(_conf['buzzer_pin'], pin_factory=rem_pi)
        log.debug("...init done!")

    # activate buzz
    def on(self,  time = 0) :
        log.debug("Activate buzz")
        if _conf['quiet'] is False :
            self.buzzer.on()
        if time is not 0 :
            sleep(time)
            self.off()

    # deactivate buzz
    def off(self) :
        log.debug("Deativate buzz")
        self.buzzer.off()

    # terminate
    def terminate(self) :
        log.debug("Buzzer termination...")
        self.buzzer.close()

# DEBUG
if __name__ == "__main__":

    log.log("Welcome! Testing Buzzer Sensor:")
    time = _conf['buzzer_wait_time']
    buzzer = RoPiBuzzer("192.168.1.118")
    try:

        log.log("Buzz!")
        buzzer.on(time)

        log.log("Silence!")
        buzzer.off()

    # capture interruption
    except KeyboardInterrupt:
        pass

    buzzer.terminate()
    del buzzer
    log.log("Goodbye!")
