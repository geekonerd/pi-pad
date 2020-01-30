# IMPORTS
from gpiozero import InputDevice, OutputDevice
from gpiozero.pins.pigpio import PiGPIOFactory
from time import sleep, time
from Logger import Logger
from multiprocessing import Process, Value
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

        # using InputDevice and OutputDevice
        rem_pi = PiGPIOFactory(host=remote_address)
        self.distance1_trig = OutputDevice(pin=_conf['trig_1_pin'], pin_factory=rem_pi)
        self.distance1_echo = InputDevice(pin=_conf['echo_1_pin'], pin_factory=rem_pi)
        self.distance2_trig = OutputDevice(pin=_conf['trig_2_pin'], pin_factory=rem_pi)
        self.distance2_echo = InputDevice(pin=_conf['echo_2_pin'], pin_factory=rem_pi)
        
        # values
        self.distance1 = Value('i', 0)
        self.distance2 = Value('i', 0)
        
        # processes
        log.debug("Initializing Distance processes...")
        self.process1 = Process(target=self.D1)
        self.process2 = Process(target=self.D2)
        self.process1.start()
        self.process2.start()
        log.debug("...init done!")

    # is close
    def is_close(self) :
        distance1 = (self.distance1.value) < _conf['SAFETY_DISTANCE']
        distance2 = (self.distance2.value) < _conf['SAFETY_DISTANCE']
        log.debug("> is close ? " + str(distance1 or distance2))
        return distance1 or distance2

    # get distance 1
    def get_distance1(self) :
        log.debug("> Distance 1: " + str(self.distance1.value))
        return self.distance1.value

    # get distance 2
    def get_distance2(self) :
        log.debug("> Distance 2: " + str(self.distance2.value))
        return self.distance2.value

    # terminate
    def terminate(self) :
        log.debug("Distance termination...")
        self.distance1_trig.close()
        self.distance1_echo.close()
        self.distance2_trig.close()
        self.distance2_echo.close()

    # control distance sensor 1
    def D1(self) :
        self.worker(self.distance1_trig, self.distance1_echo, self.distance1)

    # control distance sensor 1
    def D2(self) :
        self.worker(self.distance2_trig, self.distance2_echo, self.distance2)

    # worker
    def worker(self, trigger, echo, distance) :
        while True :
            log.debug("Wait for sensor...")
            sleep(_conf['SENSORS_OFF_SPAN'])
            log.debug("Activate trigger...")
            trigger.on()
            sleep(_conf['TRIG_SPAN'])
            log.debug("Deactivate trigger...")
            trigger.off()
            log.debug("Calculate distance...")
            distance.value = self.calculate_distance(
                self.wait_for_signal(time(), echo),
                self.wait_for_distance(time(), echo))

    # wait for pulse start
    def wait_for_signal(self, pulse_start, echo) :
        log.debug("Wait for echo...")
        while echo.is_active == False :
            pulse_start = time()
            log.debug("echo started at:" + str(pulse_start))
        return pulse_start

    # wait for pulse end
    def wait_for_distance(self, pulse_end, echo) :
        log.debug("Wait for echo back...")
        while echo.is_active == True :
            pulse_end = time()
            log.debug("echo ended at:" + str(pulse_end))
        return pulse_end

    # calculate distance
    def calculate_distance(self, pulse_start, pulse_end) :
        log.debug("Calculate pulse duration...")
        pulse_duration = pulse_end - pulse_start
        distance = pulse_duration * _conf['SPEED_OF_SOUND']
        log.debug("Distance is: " + str(distance))
        return int(distance)

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
