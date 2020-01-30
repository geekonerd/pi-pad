# IMPORTS
from gpiozero import LineSensor
from gpiozero.pins.pigpio import PiGPIOFactory
from time import sleep
from Logger import Logger
from RoPiConfiguration import track as _conf

# LOGGING
log = Logger(_conf['DEVEL_LOG'])

# ROPI TRACKING
class RoPiTrack :

    # initialize
    def __init__(self,  remote_address) :

        # set PINs on BOARD
        log.debug("Initializing Track...")
        log.debug("> track 1: " + str(_conf['track_1_pin']))
        log.debug("> track 2: " + str(_conf['track_2_pin']))

        # using LineSensor
        rem_pi = PiGPIOFactory(host=remote_address)
        self.track1 = LineSensor(_conf['track_1_pin'], pin_factory=rem_pi)
        self.track2 = LineSensor(_conf['track_2_pin'], pin_factory=rem_pi)
        log.debug("...init done!")

    # are tracks on line?
    def is_on_line(self) :
        track1 = self.track1.value  == _conf['color']
        track2 = self.track2.value  == _conf['color']
        log.debug("> is on line ?" + str(track1 and track2))
        return track1 and track2

    # is track1 on line?
    def track1_on_line(self) :
        track1 = self.track1.value == _conf['color']
        log.debug("> is track 1 on line?" + str(track1))
        return track1

    # is track2 on line?
    def track2_on_line(self) :
        track2 = self.track2.value == _conf['color']
        log.debug("> is track 2 on line?" + str(track2))
        return track2

    # terminate
    def terminate(self) :
        log.debug("Track termination...")
        self.track1.close()
        self.track2.close()

# DEBUG
if __name__ == "__main__":
    
    log.log("Welcome! Testing Track Sensors:")
    log.log("Color #0=black, #1=white: " + str(_conf['color']))
    time = _conf['track_wait_time']
    track = RoPiTrack("192.168.1.118")
    try:

        while True:

            log.log("> is track 1 on line? " + str(track.track1_on_line()))
            log.log("> is track 2 on line? " + str(track.track2_on_line()))
            log.log("> is on line ? " + str(track.is_on_line()))

            sleep(time)
    
    # capture interruption
    except KeyboardInterrupt:
        pass
    
    track.terminate()
    del track
    log.log("Goodbye!")
