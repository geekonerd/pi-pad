# IMPORTS
from gpiozero import Motor
from gpiozero.pins.pigpio import PiGPIOFactory
from time import sleep
from multiprocessing import Queue, Process, Value
from Logger import Logger
from RoPiConfiguration import motor as _conf

# LOGGING
log = Logger(_conf['DEVEL_LOG'])

# ROPI MOTOR
class RoPiMotor :

    # initialize
    def __init__(self, remote_address) :

	    # set PINs on BOARD
        log.debug("Initializing Motors...")
        log.debug("> back left PIN: " + str(_conf['motor_back_left_pin']))
        log.debug("> back right PIN: " + str(_conf['motor_back_right_pin']))
        log.debug("> front left PIN: " + str(_conf['motor_front_left_pin']))
        log.debug("> front right PIN: " + str(_conf['motor_front_right_pin']))

        # using Motor
        rem_pi = PiGPIOFactory(host=remote_address)
        self.motor1 = Motor(_conf['motor_front_left_pin'], _conf['motor_back_left_pin'], pin_factory=rem_pi)
        self.motor2 = Motor(_conf['motor_front_right_pin'], _conf['motor_back_right_pin'], pin_factory=rem_pi)

        # directions
        self.motor1_direction = Value("i", 0)
        self.motor2_direction = Value("i", 0)

        # queues and processes
        log.debug("Initializing Motors queues and processes...")
        self.queue1 = Queue()
        self.queue2 = Queue()
        self.process1 = Process(target=self.M1)
        self.process2 = Process(target=self.M2)
        self.process1.start()
        self.process2.start()
        log.debug("...init done!")

    # clean a queue
    def clearQueue(self, q) :
        while not q.empty() :
            q.get()

    # clean all queues
    def cleanQueues(self) :
        log.debug("Cleaning queues...")
        self.clearQueue(self.queue1)
        self.clearQueue(self.queue2)

    # stop the motors
    def stop(self) :
        self.cleanQueues()
        self.motor1.stop()
        self.motor2.stop()

    # control motor process 1
    def M1(self) :
        self.worker(self.motor1, self.queue1)

    # control motor process 2
    def M2(self) :
        self.worker(self.motor2, self.queue2)

    # worker
    def worker(self, motor, queue) :
        try :
            while True :

                if not queue.empty() :
                    direction = queue.get().split("|")
                    acceleration = float(direction[2])
                    speed = float(direction[1])
                    direction = direction[0]
                    log.debug("Going direction [" + str(direction) + "] at [" + str(speed) + "] speed for " + str(acceleration) + "s")
                    if direction == "f" :
                        motor.forward(speed=speed)
                    elif direction == "b" :
                        motor.backward(speed=speed)
                    sleep(acceleration)
                    motor.stop()

        except KeyboardInterrupt:
            pass

    # go forward
    def forward(self, speed = 1,  duration = _conf['ACCELERATION_TIME']) :
        if not self.motor1_direction.value == 1 :
            self.clearQueue(self.queue1)
        self.motor1_direction.value = 1
        if not self.motor2_direction.value == 1 :
            self.clearQueue(self.queue2)
        self.motor2_direction.value = 1
        self.queue1.put("f|" + str(speed) + "|" + str(duration))
        self.queue2.put("f|" + str(speed) + "|" + str(duration))

    # go backward
    def backward(self, speed = 1,  duration = _conf['ACCELERATION_TIME']) :
        if not self.motor1_direction.value == -1 :
            self.clearQueue(self.queue1)
        self.motor1_direction.value = -1
        if not self.motor2_direction.value == -1 :
            self.clearQueue(self.queue2)
        self.motor2_direction.value = -1
        self.queue1.put("b|" + str(speed) + "|" + str(duration))
        self.queue2.put("b|" + str(speed) + "|" + str(duration))

    # go forward LEFT
    def forwardleft(self, speed = 1,  duration = _conf['ACCELERATION_TIME']) :
        self.clearQueue(self.queue2)
        if not self.motor1_direction.value == 1 :
            self.clearQueue(self.queue1)
        self.motor1_direction.value = 1
        self.queue1.put("f|" + str(speed) + "|" + str(duration))

    # go forward RIGHT
    def forwardright(self, speed = 1,  duration = _conf['ACCELERATION_TIME']) :
        self.clearQueue(self.queue1)
        if not self.motor2_direction == 1 :
            self.clearQueue(self.queue2)
        self.motor2_direction.value = 1
        self.queue2.put("f|" + str(speed) + "|" + str(duration))

    # go backward LEFT
    def backwardleft(self, speed = 1,  duration = _conf['ACCELERATION_TIME']) :
        self.clearQueue(self.queue2)
        if not self.motor1_direction.value == -1 :
            self.clearQueue(self.queue1)
        self.motor1_direction.value = -1
        self.queue1.put("b|" + str(speed) + "|" + str(duration))

    # go backward RIGHT
    def backwardright(self, speed = 1,  duration = _conf['ACCELERATION_TIME']) :
        self.clearQueue(self.queue1)
        if not self.motor2_direction.value == -1 :
            self.clearQueue(self.queue2)
        self.motor2_direction.value = -1
        self.queue2.put("b|" + str(speed) + "|" + str(duration))

    # terminate
    def terminate(self) :
        log.debug("Motors termination...")
        self.process1.terminate()
        self.process2.terminate()
        self.stop()
        self.queue1.close()
        self.queue1.join_thread()
        self.queue2.close()
        self.queue2.join_thread()
        self.motor1.close()
        self.motor2.close()

# DEBUG
if __name__ == "__main__":

    log.log("Welcome! Testing Motors:")
    time = _conf['motor_acceleration_time']
    wait = _conf['motor_wait_time']
    motor = RoPiMotor("192.168.1.118")
    try :

        log.log("Forward...")
        motor.forward(duration=time)
        sleep(wait)

        log.log("F-Left...")
        motor.forwardleft(duration=time)
        sleep(wait)

        log.log("Left...")
        motor.forwardleft(speed=0.5,  duration=time)
        sleep(wait)

        log.log("F-Right...")
        motor.forwardright(duration=time)
        sleep(wait)

        log.log("Right...")
        motor.forwardright(speed=0.5,  duration=time)
        sleep(wait)

        log.log("Backward...")
        motor.backward(duration=time)
        sleep(wait)

        log.log("B-Left...")
        motor.backwardleft(duration=time)
        sleep(wait)

        log.log("B-Right...")
        motor.backwardright(duration=time)
        sleep(wait)

    # capture interruption
    except KeyboardInterrupt:
        pass

    motor.terminate()
    del motor
    log.log("Goodbye!")
