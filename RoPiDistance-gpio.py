# IMPORTS
from gpiozero import DistanceSensor
from gpiozero.pins.pigpio import PiGPIOFactory
from time import sleep
from Logger import Logger
from RoPiConfiguration import distance as _conf

# LOGGER
log = Logger(_conf['DEVEL_LOG'])

# ROPI DISTANCE!
class RoPiDistance :

    # initialization
    def __init__(self, remote_address) :

        # set PINs on BOARD
        log.debug("Initializing Distance...")
        log.debug("> echo 1 pin: " + str(_conf['echo_1_pin']))
        log.debug("> trig 1 pin: " + str(_conf['trig_1_pin']))
        log.debug("> echo 2 pin: " + str(_conf['echo_2_pin']))
        log.debug("> trig 2 pin: " + str(_conf['trig_2_pin']))

        # using DistanceSensor
        rem_pi = PiGPIOFactory(host=remote_address)
        self.distance1 = DistanceSensor(echo=_conf['echo_1_pin'], trigger=_conf['trig_1_pin'], pin_factory=rem_pi)
        self.distance2 = DistanceSensor(echo=_conf['echo_2_pin'], trigger=_conf['trig_2_pin'], pin_factory=rem_pi)
        log.debug("...init done!")

    # is close
    def is_close(self) :
        distance1 = (self.distance1.distance * 100) < _conf['SAFETY_DISTANCE']
        distance2 = (self.distance2.distance * 100) < _conf['SAFETY_DISTANCE']
        log.debug("> is close ?" + str(distance1 or distance2))
        return distance1 or distance2

    # get distance 1
    def get_distance1(self) :
        log.debug("> Distance 1: " + str(self.distance1.distance * 100))
        return self.distance1.distance * 100

    # get distance 2
    def get_distance2(self) :
        log.debug("> Distance 2: " + str(self.distance2.distance * 100))
        return self.distance2.distance * 100

    # terminate
    def terminate(self) :
        log.debug("Distance termination...")
        self.distance1.close()
        self.distance2.close()

# DEBUG
if __name__ == "__main__":

    log.log("Welcome! Testing Distance Sensors:")
    log.log("Safety distance: " + str(_conf['SAFETY_DISTANCE']))
    distance = RoPiDistance("192.168.1.118")
    try:
        while True:

            log.log("Distance 1: " + str(distance.get_distance1()))
            log.log("Distance 2: " + str(distance.get_distance2()))
            log.log("is close ?: " + str(distance.is_close()))

            sleep(_conf['distance_wait_time'])

    # capture interruption
    except KeyboardInterrupt:
        pass

    distance.terminate()
    del distance
    log.log("Goodbye!")
