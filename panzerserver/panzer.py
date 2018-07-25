import time
import enum

from panzerserver.watcher import WatchLoop

try:
    from RPi import GPIO
    GPIO.setmode(GPIO.BOARD)  # Use board number
except ImportError:
    import fake_rpi
    from fake_rpi.RPi import GPIO


    def toggle_fake_print(p):
        fake_rpi.toggle_print(p)


class Component(object):

    def initialize(self):
        raise NotImplementedError


class DriveDirection(enum.Enum):
    STOP = 0
    FORWARD = 1
    BACKWARD = 2
    BRAKE = 3


class Wheel(Component):

    def __init__(self, channel1, channel2, channel_pwm=None):
        self.channel1 = channel1
        self.channel2 = channel2
        self.channel_pwm = channel_pwm
        self.pwm = None
        self.is_pwm_active = False

    def initialize(self):
        print("setup GPIO OUT %d %d" % (self.channel1, self.channel2))
        GPIO.setup(self.channel1, GPIO.OUT)
        GPIO.setup(self.channel2, GPIO.OUT)
        GPIO.setup(self.channel_pwm, GPIO.OUT)
        self.pwm = GPIO.PWM(self.channel_pwm, 1000)  # TODO check frequency

    def pwm_start(self, level):
        """Start PWM

        :param level: duty ratio [0, 1.0]
        :return: None
        """
        # set duty to 0..100
        duty = int(level * 100)
        duty = min(duty, 100)
        duty = max(duty, 0)

        if not self.is_pwm_active:
            self.is_pwm_active = True
            self.pwm.start(duty)
        else:
            self.pwm.ChangeDutyCycle(duty)

    def forward(self, level):
        GPIO.output(self.channel1, GPIO.HIGH)
        GPIO.output(self.channel2, GPIO.LOW)
        self.pwm_start(level)

    def backward(self, level):
        GPIO.output(self.channel1, GPIO.LOW)
        GPIO.output(self.channel2, GPIO.HIGH)
        self.pwm_start(level)

    def brake(self, level=None):
        GPIO.output(self.channel1, GPIO.HIGH)
        GPIO.output(self.channel2, GPIO.HIGH)

    def stop(self):
        GPIO.output(self.channel1, GPIO.LOW)
        GPIO.output(self.channel2, GPIO.LOW)
        self.pwm.stop()
        self.is_pwm_active = False

    def drive(self, direction, level=1.0):
        level = abs(level)
        # normalize level
        if level > 1:
            level = 1

        if direction == DriveDirection.FORWARD:
            self.forward(level)
        elif direction == DriveDirection.BACKWARD:
            self.backward(level)
        elif direction == DriveDirection.BRAKE:
            self.brake(level)
        else:
            self.stop()


class Controller(object):
    WATCH_INTERVAL = 1  # msec
    WATCH_THRESHOLD = 3  # msec

    class MethodEnum(enum.Enum):
        DRIVE = "DRIVE"
        MOVE_TURRET = "MOVE_TURRET"

    def __init__(self,
                 l_channel1, l_channel2, l_pwm,
                 r_channel1, r_channel2, r_pwm,
                 ):
        # Components
        self.l_wheel = Wheel(l_channel1, l_channel2, l_pwm)
        self.r_wheel = Wheel(r_channel1, r_channel2, r_pwm)

        self.last_updated = 0
        self.is_init = False

        self.watch = WatchLoop()
        self.watch.set_callback(Controller.MethodEnum.DRIVE, self.stop_drive)

    def initialize(self):
        self.l_wheel.initialize()
        self.r_wheel.initialize()
        self.is_init = True

    def is_initialized(self):
        return self.is_init

    def cleanup(self):
        GPIO.cleanup()

    def stop_all(self):
        print("stop all")
        self.l_wheel.stop()
        self.r_wheel.stop()

    def watch_loop(self):
        self.watch.start()

    def set_watch_threshold(self, threshold_msec):
        self.watch.set_thresold(threshold_msec)

    @staticmethod
    def level_to_direction(level):
        if level > 0:
            return DriveDirection.FORWARD
        elif level < 0:
            return DriveDirection.BACKWARD
        return DriveDirection.STOP

    def drive(self, l_level, r_level):
        l_direction = self.level_to_direction(l_level)
        r_direction = self.level_to_direction(r_level)

        self.l_wheel.drive(l_direction, abs(l_level))
        self.r_wheel.drive(r_direction, abs(r_level))

        self.watch.record(Controller.MethodEnum.DRIVE)

    def stop_drive(self):
        self.l_wheel.stop()
        self.r_wheel.stop()


if __name__ == '__main__':
    import concurrent.futures

    con = Controller(
        11, 13, None,  # left wheel
        15, 16, None,  # right wheel
    )
    con.initialize()

    executor = concurrent.futures.ThreadPoolExecutor()
    executor.submit(con.watch_loop)

    print("go")
    con.drive(1, 1)
    GPIO.cleanup()
