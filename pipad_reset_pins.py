from gpiozero import DigitalOutputDevice
from Logger import Logger
from PiPadConfiguration import PiPadConfiguration as _conf

log = Logger(_conf['DEVEL_LOG'])

# set used pins
used_pins = [14, 15, 17, 18, 27, 5, 6, 13, 16]

log.log("Resetting all used PINs")
log.log("> " + str(used_pins))

# reset used PINs
for pin in used_pins :
    log.debug("Closing PIN: " + str(pin))
    _p = DigitalOutputDevice(pin)
    _p.off()

log.log("RESET DONE!")
