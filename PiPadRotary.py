# IMPORTS
from time import sleep
from gpiozero import Button,  InputDevice
from multiprocessing import Process, Value
from Logger import Logger
from PiPadConfiguration import rotary as _conf

# LOGGER
log = Logger(_conf['DEVEL_LOG'])

# PiPAD ROTARY ENCODER
class PiPadRotary:

    # initialize
    def __init__(self) :

        # set PINs on BOARD
        log.debug("Initializing Rotary Encoder...")
        log.debug("> Button:" + str(_conf['btn_pin']))
        self.btn = Button(_conf['btn_pin'])
        log.debug("> Clock:" + str(_conf['clock_pin']))
        self.clock = InputDevice(_conf['clock_pin'])
        log.debug("> DT:" + str(_conf['dt_pin']))
        self.dt = InputDevice(_conf['dt_pin'])

        # values
        self.counter = Value('i', 0)

        # processes
        log.debug("Initializing Rotary processes...")
        self.process = Process(target=self.worker)
        self.process.start()
        log.debug("...init done!")

    # get counter
    def get_counter(self) :
        return self.counter.value

    # set counter
    def set_counter(self, value) :
        self.counter.value = value

    # reset counter
    def reset_counter(self) :
        self.counter.value = 0

    # check button pressed
    def is_pressed(self) :
        return self.btn.is_pressed

    # control rotary
    def worker(self) :
        try :
                clock_value = self.clock.value
                while True :

                    clock = self.clock.value
                    dt = self.dt.value
                    log.debug("Clock: " + str(clock_value))
                    log.debug("Current Clock: " + str(clock))
                    log.debug("DT: " + str(dt))
                    if clock != clock_value :
                        if dt != clock :
                            log.debug("!=")
                            self.counter.value += 1
                        else :
                            log.debug("==")
                            self.counter.value -= 1
                    clock_value = clock
                    sleep(_conf['clock_wait_time'])

        except KeyboardInterrupt:
            pass

    # terminate
    def terminate(self) :
        log.debug("Rotary Encoder termination...")
        self.btn.close()
        self.dt.close()
        self.clock.close()
        self.process.join()
        self.process.terminate()

# DEBUG
if __name__ == "__main__":

    log.log("Welcome! Testing Rotary Encoder:")
    rotary = PiPadRotary()

    try :
        counter = rotary.get_counter()
        while True:
            
            current_counter = rotary.get_counter()
            if current_counter != counter :
                counter = current_counter
                log.log("Counter: " + str(counter))
            if (rotary.is_pressed()) :
                log.log("Rotary button pressed!")

            sleep(_conf['btn_wait_time'])

    # capture interruption
    except KeyboardInterrupt:
        pass

    rotary.terminate()
    del rotary
    log.log("Goodbye!")
