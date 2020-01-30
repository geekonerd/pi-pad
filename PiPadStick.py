# IMPORTS
from time import sleep
from gpiozero import Button
from multiprocessing import Process, Value
import board
import busio
import adafruit_ads1x15.ads1015 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
from Logger import Logger
from PiPadConfiguration import stick as _conf

# LOGGING
log = Logger(_conf['DEVEL_LOG'])

# PiPAD STICK
class PiPadStick:

    # initialization
    def __init__(self) :

        # set PINs on BOARD
        log.debug("Initializing Stick...")
        log.debug("> button " + str(_conf['btn_pin']))
        self.btn = Button(_conf['btn_pin'])

        # initialize ADC
        i2c = busio.I2C(board.SCL, board.SDA)
        self.ads = ADS.ADS1015(i2c)

        # values
        self.x = Value('i', 0)
        self.y = Value('i', 0)

        # processes
        log.debug("Initializing Stick processes...")
        self.process = Process(target=self.worker)
        self.process.start()
        log.debug("...init done!")

    # is stick pressed
    def is_pressed(self) :
        return self.btn.is_pressed

    # x value
    def xAxisValue(self) :
        return self.x.value

    # y value
    def yAxisValue(self) :
        return self.y.value

    # current position
    def position(self) :
        min = _conf['min']
        max = _conf['max']
        x = self.xAxisValue()
        y = self.yAxisValue()

        if (x > min and x < max and y > min and y < max) :
            log.debug("Stick is held")
            return 0
        elif (x > min and x < max) :
            if (y < min) :
                log.debug("Stick right")
                return 7
            elif (y > max) :
                log.debug("Stick left")
                return 3
        elif (x < min) :
            if (y > min and y < max) :
                log.debug("Stick up")
                return 1
            elif (y < min) :
                log.debug("Stick up right")
                return 8
            elif (y > max) :
                log.debug("Stick up left")
                return 2
        elif (x > max) :
            if (y > min and y < max) :
                log.debug("Stick down")
                return 5
            elif (y < min) :
                log.debug("Stick down right")
                return 6
            elif (y > max) :
                log.debug("Stick down left")
                return 4

    # control axis
    def worker(self) :
        try :
            while True :

                val_x = AnalogIn(self.ads, ADS.P1)
                val_y = AnalogIn(self.ads, ADS.P0)
                self.x.value = val_x.value
                self.y.value = val_y.value
                sleep(_conf['axis_wait_time'])

        except KeyboardInterrupt:
            pass

    # terminate
    def terminate(self) :
        log.debug("Stick termination...")
        self.btn.close()
        self.process.join()
        self.process.terminate()

# DEBUG
if __name__ == "__main__":

    log.log("Welcome! Testing Axis:")
    stick = PiPadStick()

    log.log("Stick positions:")
    log.log("N: 1, NW: 2, W: 3, SW: 4, S: 5, SE: 6, E: 7, NE: 8")

    try:
        while True:

            if (stick.is_pressed() == True) :
                log.log("Stick button pressed!")

            position = stick.position()
            if position is not 0 :
                log.log("Stick position: " + str(position))

            sleep(_conf['btn_wait_time'])

    # capture interruption
    except KeyboardInterrupt:
        pass

    stick.terminate()
    del stick
    log.log("Goodbye!")
