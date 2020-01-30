from gpiozero import DigitalOutputDevice
from gpiozero.pins.pigpio import PiGPIOFactory
from Logger import Logger
from RoPiConfiguration import RoPiConfiguration as _conf

log = Logger(_conf['DEVEL_LOG'])

# set used pins
used_pins = [4, 27, 17, 22, 18, 12, 23, 24, 26, 25, 20, 21, 16, 5, 6, 16, 2, 4, 10, 9, 19, 8, 7, 11, 13]

log.log("Resetting all used PINs")
log.log("> " + str(used_pins))

rem_pi = PiGPIOFactory(host=_conf['remote_address'])

# reset used PINs
for pin in used_pins :
    log.debug("Closing PIN: " + str(pin))
    _p = DigitalOutputDevice(pin, pin_factory=rem_pi)
    _p.off()
    _p.close()

log.log("RESET DONE!")
