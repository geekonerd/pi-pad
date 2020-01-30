# IMPORTS
""" imports all the libraries and PiPAD + RoPi sensors """
import sys
from time import sleep
from Logger import Logger
from multiprocessing import Process
from PiPadConfiguration import PiPadConfiguration as _pipad
from PiPadButtons import PiPadButtons
from PiPadLED import PiPadLED
from PiPadStick import PiPadStick
from PiPadRotary import PiPadRotary
from RoPiConfiguration import RoPiConfiguration as _ropi
from RoPiLED import RoPiLED
from RoPiBuzzer import RoPiBuzzer
from RoPiServo import RoPiServo
from RoPiTrack import RoPiTrack
from RoPiDistance import RoPiDistance
#from RoPiScreen import RoPiScreen
from RoPiMotor import RoPiMotor

# SENSORS
""" instantiate PiPAD + RoPi sensors """
pipad_led = PiPadLED()
pipad_buttons = PiPadButtons()
pipad_stick = PiPadStick()
pipad_rotary = PiPadRotary()
ropi_led = RoPiLED(_ropi['remote_address'])
ropi_buzzer = RoPiBuzzer(_ropi['remote_address'])
ropi_servo = RoPiServo(_ropi['remote_address'])
ropi_track = RoPiTrack(_ropi['remote_address'])
ropi_distance = RoPiDistance(_ropi['remote_address'])
#ropi_screen = RoPiScreen(_ropi['remote_address'])
ropi_motor = RoPiMotor(_ropi['remote_address'])

# LOGGING
""" instantiate logger """
log = Logger(_pipad['DEVEL_LOG'])

# GLOBALS
""" global variables """
rotary_counter_lr = 0
rotary_current_counter_lr = 0
rotary_counter_ud = 0
rotary_current_counter_ud = 0
rotary_reverse = 0
stick_autonomous = False
stick_position = 0

# COLOR A LED
""" color a specified RGBLEB *to_color* *for_time* """
def led(led, to_color = "white", for_time = _pipad['led_active_time']) : 
    led.color(to_color, for_time)
def led_pipad(to_color, for_time = _pipad['led_active_time']) :
    led(pipad_led, to_color, for_time)
def led_ropi(to_color, for_time = _pipad['led_active_time']) :
    led(ropi_led, to_color, for_time)

# BUZZ
""" make a buzz *for_time* """
def buzz(for_time = _pipad['clacson_active_time']) :
    ropi_buzzer.on(for_time)

# RESET SERVO
""" reset the position of the camera """
def camera_reset() :
    global rotary_counter_lr
    global rotary_current_counter_lr
    global rotary_counter_ud
    global rotary_current_counter_ud
    
    rotary_counter_lr = 0
    rotary_current_counter_lr = 0
    rotary_counter_ud = 0
    rotary_current_counter_ud = 0
    ropi_servo.reset()
    pipad_rotary.reset_counter()

# MOVE CAMERA
""" move camera *to_position* """
def move_camera(to_position) :
    to_position()

# MOVE MOTOR
""" move motors *to_direction* *with_speed* """
def move_motor(to_direction = False, with_speed = 1) :
    if to_direction is not False :
        to_direction(with_speed)

# BTN1 PRESSED
""" reset the position of the camera and color LEDs to magenta """
def button1_pressed() :
    process1 = Process(target=led_pipad, args=('magenta',))
    process2 = Process(target=led_ropi, args=('magenta',))
    process3 = Process(target=camera_reset)
    process1.start()
    process2.start()
    process3.start()
    log.debug("BTN1 pressed!")

# BTN2 PRESSED
""" make a buzz and color LEDs to blue """
def button2_pressed() :
    process1 = Process(target=led_pipad, args=('blue',))
    process2 = Process(target=led_ropi, args=('blue',))
    process3 = Process(target=buzz)
    process1.start()
    process2.start()
    process3.start()
    log.debug("BTN2 pressed!")

# ROTARY PRESSED
""" reverse servo to rotate and color LEDs to white """
def rotary_pressed() :
    global rotary_reverse
    rotary_reverse = (rotary_reverse + 1) % 2
    if (rotary_reverse == 0) :
        pipad_rotary.set_counter(rotary_current_counter_lr)
    else :
        pipad_rotary.set_counter(rotary_current_counter_ud)
    process1 = Process(target=led_pipad, args=('white',))
    process2 = Process(target=led_ropi, args=('white',))
    process1.start()
    process2.start()
    log.debug("BTN Rotary pressed!")

# ROTARY ROTATED
""" check if ROTARY is rotated and check servo direction to rotate the camera """
def rotary_rotated() :
    global rotary_counter_lr
    global rotary_current_counter_lr
    global rotary_counter_up
    global rotary_current_counter_up
    global rotary_reverse
    if rotary_reverse == 0 :
        log.debug("Rotary counter LR: " + str(rotary_current_counter_lr))
        if rotary_counter_lr > rotary_current_counter_lr :
            log.debug("Move camera left")
            process = Process(target=move_camera, args=(ropi_servo.move_left,))
            process.start()
        else :
            log.debug("Move camera right")
            process = Process(target=move_camera, args=(ropi_servo.move_right,))
            process.start()
    else :
        log.debug("Rotary counter UP: " + str(rotary_current_counter_ud))
        if rotary_counter_ud > rotary_current_counter_ud :
            log.debug("Move camera down")
            process = Process(target=move_camera, args=(ropi_servo.move_down,))
            process.start()
        else :
            log.debug("Move camera up")
            process = Process(target=move_camera, args=(ropi_servo.move_up,))
            process.start()

# STICK PRESSED
""" check if STICK is pressed and activate autonomous guide and color LEDs to yellow """
def stick_pressed() :
    global stick_autonomous
    log.debug("Stick pressed!")
    if stick_autonomous is False :
        stick_autonomous = True
        process1 = Process(target=led_pipad, args=('yellow',))
        process2 = Process(target=led_ropi, args=('yellow',))
        process3 = Process(target=position_autonomous)
        process1.start()
        process2.start()
        process3.start()
    else :
        process1 = Process(target=led_pipad, args=('cyan',))
        process2 = Process(target=led_ropi, args=('cyan',))
        process1.start()
        process2.start()

# POSITION CHANGED
""" deactivate autonomous guide and move RoPi to direction """
def position_changed():
    global stick_autonomous
    global stick_position

    # all the directions
    directions = {
        0 : move_motor, 
        1 : position_forward , 
        2 : position_forwardleft, 
        3 : position_left, 
        4 : position_backwardleft, 
        5 : position_backward, 
        6 : position_backwardright, 
        7 : position_right, 
        8 : position_forwardright
    }

    log.debug("Stick position: " + str(stick_position))
    stick_autonomous = False
    directions.get(stick_position, lambda: position_unknown)()

# POSITION CHECK
""" check for obstacles """
def position_check() :
    log.debug("Check for obstacles...")
    if ropi_distance.is_close() == False :
        # let's go!
        return True
    else :
        # dont' move! and color LEDs to red
        led(pipad_led, "red")
        led(ropi_led, "red")
        return False

# POSITION FORWARD
""" go forward! """
def position_forward() :
    log.debug("Going forward...")
    if position_check() is True :
        move_motor(ropi_motor.forward)

# POSITION FORWARD LEFT
""" go forward left! """
def position_forwardleft() :
    log.debug("Going forward left...")
    if position_check() is True :
        move_motor(ropi_motor.forwardleft)

# POSITION LEFT
""" go left! """
def position_left() :
    log.debug("Going left...")
    if position_check() is True :
        move_motor(ropi_motor.forwardleft, 0.5)
    
# POSITION BACKWARD LEFT
""" go backward! """
def position_backwardleft() :
    log.debug("Going backward left...")
    move_motor(ropi_motor.backwardleft)
    
# POSITION BACKWARD
#async def position_backward() :
def position_backward() :
    log.debug("Going backward...")
    move_motor(ropi_motor.backward)
    
# POSITION BACKWARD RIGHT
""" go backward right! """
def position_backwardright() :
    log.debug("Going backward right...")
    move_motor(ropi_motor.backwardright)
    
# POSITION RIGHT
""" go right! """
def position_right() :
    log.debug("Going right...")
    if position_check is True :
        move_motor(ropi_motor.forwardright, 0.5)
    
# POSITION FORWARD RIGHT
""" go forward right! """
def position_forwardright() :
    log.debug("Going forward right...")
    if position_check is True :
        move_motor(ropi_motor.forwardright)

# POSITION AUTONOMOUS
""" go autonomous! """
def position_autonomous() :
    global stick_autonomous
    log.debug("Autonomous Mode")
    while True :
        if stick_autonomous is True :
            log.debug("Calculate...")
            # TODO: go autonomous

# POSITION UNKNOWN
""" position requested doesn't exist """
def position_unknown() :
    log.error("Position Unknown!")
    process1 = Process(target=led_pipad, args=('red',))
    process2 = Process(target=led_ropi, args=('red',))
    process1.start()
    process2.start()

# PiPAD!
""" PiPAD controls RoPi in asynchronous way by event based actions """
if __name__ == "__main__" :

    # init
    log.log("Welcome to PiPAD!")
    process1 = Process(target=led_pipad, args=('green',))
    process2 = Process(target=led_ropi, args=('green',))
    process1.start()
    process2.start()

    # listen for input
    log.debug("Waiting for input...")
    try :

        # run forever
        while True :
        
            if pipad_buttons.is_button1_pressed() is True :
                button1_pressed()

            if pipad_buttons.is_button2_pressed() is True :
                button2_pressed()

            if pipad_stick.is_pressed() == True :
                stick_pressed()

            stick_position = pipad_stick.position()
            position_changed()

            if pipad_rotary.is_pressed() == True :
                rotary_pressed()

            if (rotary_reverse == 0) :
                rotary_current_counter_lr = pipad_rotary.get_counter()
            else :
                rotary_current_counter_ud = pipad_rotary.get_counter()
            if rotary_current_counter_lr != rotary_counter_lr or rotary_current_counter_ud != rotary_counter_ud :
                rotary_rotated()
                if (rotary_reverse == 0) :
                    rotary_counter_lr = rotary_current_counter_lr
                else :
                    rotary_counter_ud = rotary_current_counter_ud

            sleep(_pipad['CYCLE_WAIT_TIME'])

    # exit on CTRL+C
    except KeyboardInterrupt:
        log.debug("Exiting...")
        sys.stderr.flush()
        pass

    # clean up!
    pipad_led.terminate()
    pipad_buttons.terminate()
    pipad_stick.terminate()
    pipad_rotary.terminate()
    ropi_led.terminate()
    ropi_buzzer.terminate()
    ropi_servo.terminate()
    ropi_track.terminate()
    ropi_distance.terminate()
    #ropi_screen.terminate()
    ropi_motor.terminate()
    del pipad_led
    del pipad_buttons
    del pipad_stick
    del pipad_rotary
    del ropi_led
    del ropi_buzzer
    del ropi_servo
    del ropi_track
    del ropi_distance
    #del ropi_screen
    del ropi_motor

    log.log("Goodbye!")
