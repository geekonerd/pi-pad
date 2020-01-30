# IMPORTS
from gpiozero import Servo
from gpiozero.pins.pigpio import PiGPIOFactory
from time import sleep
from multiprocessing import Queue, Process, Value
from Logger import Logger
from RoPiConfiguration import servo as _conf

# LOGGING
log = Logger(_conf['DEVEL_LOG'])

# ROPI SERVO!
class RoPiServo :

    # initialize
    def __init__(self, remote_address) :

        # set PINs on BOARD
        log.debug("Initializing Servos...")
        log.debug("> pin 1: " + str(_conf['servo_1_pin']))
        log.debug("> pin 2: " + str(_conf['servo_2_pin']))

        # using Servo
        rem_pi = PiGPIOFactory(host=remote_address)
        self.servo1 = Servo(_conf['servo_1_pin'], pin_factory=rem_pi)
        self.servo2 = Servo(_conf['servo_2_pin'], pin_factory=rem_pi)

        # servos positions
        self.servo1_position = Value('d', 0.5)
        self.servo2_position = Value('d', 0.5)

        # queues and processes
        log.debug("Initializing Servos queues and processes...")
        self.queue1 = Queue()
        self.queue2 = Queue()
        self.process1 = Process(target=self.P1)
        self.process2 = Process(target=self.P2)
        self.process1.start()
        self.process2.start()
        log.debug("...init done!")

    # clean all queues
    def cleanQueues(self) :
        log.debug("Cleaning queues...")
        self.clearQueue(self.queue1)
        self.clearQueue(self.queue2)

    # clean queue
    def clearQueue(self, q) :
        while not q.empty() :
            q.get()

    # move servos
    def move_servo1(self, amount) :
        self.queue1.put(amount)
    def move_servo2(self, amount) :
        self.queue2.put(amount)

    # go UP
    def move_up(self) :
         self.move_servo1(-0.1)

    # go DOWN
    def move_down(self) :
         self.move_servo1(0.1)

    # go LEFT
    def move_left(self) :
         self.move_servo2(0.1)

    # go RIGHT
    def move_right(self) :
         self.move_servo2(-0.1)

    # reset position
    def reset(self) :
        self.cleanQueues()
        self.servo1_position.value = 0.5
        self.servo1.mid()
        self.servo2_position.value = 0.5
        self.servo2.mid()

    # control process 1
    def P1(self) :
        self.worker(self.servo1, self.servo1_position, self.queue1)

    # control process 2
    def P2(self) :
        self.worker(self.servo2, self.servo2_position, self.queue2)

    # worker
    def worker(self, servo, position, queue) :
        try :
            while True :

              if not queue.empty() :
                  value = queue.get()
                  value = position.value + value
                  log.debug("Moving to: " + str(value))
                  if value > -1 and value < 1 :
                      position.value = value
                      servo.value = value

        except KeyboardInterrupt:
            pass

    # terminate
    def terminate(self) :
        log.debug("Servos termination...")
        self.process1.terminate()
        self.process2.terminate()
        self.reset()
        self.queue1.close()
        self.queue1.join_thread()
        self.queue2.close()
        self.queue2.join_thread()
        sleep(_conf['servo_reset_time'])
        self.servo1.close()
        self.servo2.close()

# DEBUG
if __name__ == "__main__":

    log.log("Welcome! Testing Servos:")
    time = _conf['servo_wait_time']
    servo = RoPiServo("192.168.1.118")

    try :

        log.log("Reset...")
        servo.reset()
        sleep(time)

        log.log("Go up...")
        for x in range(15):
            servo.move_up()
        sleep(time)

        log.log("Go left...")
        for x in range(20):
            servo.move_left()
        sleep(time)

        log.log("Go right...")
        for x in range(5):
            servo.move_right()
        sleep(time)

        log.log("Go down...")
        for x in range(10):
            servo.move_down()
        sleep(time)
    
    # capture interruption
    except KeyboardInterrupt:
        pass
    
    servo.terminate()
    del servo
    log.log ("Goodbye!")
