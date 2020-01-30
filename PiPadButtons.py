# IMPORTS
from time import sleep
from gpiozero import Button
from Logger import Logger
from PiPadConfiguration import buttons as _conf

# LOGGING
log = Logger(_conf['DEVEL_LOG'])

# PiPAD BUTTONS
class PiPadButtons :

    # initialization
    def __init__(self) :

        # buttons
        log.debug("Initializing Buttons...")
        log.debug("> button 1 pin: " + str(_conf['btn1_pin']))
        self.btn1 = Button(_conf['btn1_pin'])
        log.debug("> button 2 pin: " + str(_conf['btn2_pin']))
        self.btn2 = Button(_conf['btn2_pin'])
        log.debug("...init done!")

    # is button 1 pressed ?
    def is_button1_pressed(self) :
        return self.btn1.is_pressed

    # is button 2 pressed ?
    def is_button2_pressed(self) :
        return self.btn2.is_pressed

    # terminate
    def terminate(self) :
        log.debug("Buttons termination...")
        self.btn1.close()
        self.btn2.close()

# DEBUG
if __name__ == "__main__":

    # init
    log.log("Welcome! Testing Buttons:")
    buttons = PiPadButtons()
    try:

        # wait for input
        log.debug("Waiting for input...")
        while True:

            if (buttons.is_button1_pressed() == True) :
                log.log("BTN1 pressed!")

            if (buttons.is_button2_pressed() == True) :
                log.log("BTN2 pressed!")

            sleep(_conf['btn_wait_time'])

    # capture interruption
    except KeyboardInterrupt:
        pass

    # bye bye
    buttons.terminate()
    del buttons
    log.log("Goodbye!")
