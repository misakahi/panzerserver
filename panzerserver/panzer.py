import time
import enum
import functools

from panzerserver.watcher import WatchLoop

try:
    from RPi import GPIO
    GPIO.setmode(GPIO.BCM)  # Use board number
except ImportError:
    import fake_rpi
    from fake_rpi.RPi import GPIO


    def toggle_fake_print(p):
        fake_rpi.toggle_print(p)


class Component(object):

    def __init__(self):
        self._is_initialized = False

    def initialize(self):
        self._is_initialized = True

    def is_initialized(self):
        return self._is_initialized


class DriveDirection(enum.Enum):
    STOP = 0
    FORWARD = 1
    BACKWARD = 2
    BRAKE = 3


class Wheel(Component):

    PWM_FREQUENCY = 50    # Hz

    def __init__(self, channel1, channel2, channel_pwm=None):
        super(Wheel, self).__init__()

        self.channel1 = channel1
        self.channel2 = channel2
        self.channel_pwm = channel_pwm
        self.pwm = None     # initialized later
        self.is_pwm_active = False

    def initialize(self):
        super(Wheel, self).initialize()

        print("setup GPIO OUT %d %d" % (self.channel1, self.channel2))
        GPIO.setup(self.channel1, GPIO.OUT)
        GPIO.setup(self.channel2, GPIO.OUT)
        if self.channel_pwm is not None:
            GPIO.setup(self.channel_pwm, GPIO.OUT)
            self.pwm = GPIO.PWM(self.channel_pwm, self.PWM_FREQUENCY)  # TODO check frequency

    def pwm_start(self, level):
        """Start PWM

        :param level: duty ratio [0, 1.0]
        :return: None
        """
        if self.channel_pwm is None:
            return

        # set duty to 0..100
        duty = int(level * 100)
        duty = min(duty, 100)
        duty = max(duty, 0)

        if not self.is_pwm_active:
            self.is_pwm_active = True
            self.pwm.start(duty)
        else:
            self.pwm.ChangeDutyCycle(duty)

    def pwm_stop(self):
        if self.channel_pwm is None:
            return
        self.pwm.stop()

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
        self.pwm_stop()
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


class Turret(Component):

    def __init__(self,
                 channel1, channel2, pwm,
                 servo):
        super(Turret, self).__init__()

        self.rot = Wheel(channel1, channel2, pwm)
        self.servo = servo

    def initialize(self):
        super(Turret, self).initialize()

        self.rot.initialize()
        # TODO servo

    def rotate(self, val):
        """Rotate turret

        :param val:
        :return: None
        """
        level = min(1, abs(val))
        if level == 0:
            return
        if val > 0:
            direction = DriveDirection.FORWARD
        else:
            direction = DriveDirection.BACKWARD

        self.rot.drive(direction, level)

    def updown(self, val):
        """Up/Down the barrel

        :param val:
        :return:
        """
        # TODO implement updown barrel
        pass

    def stop(self):
        self.rot.stop()


class Controller(Component):
    WATCH_INTERVAL = 1  # msec
    WATCH_THRESHOLD = 3  # msec

    class MethodEnum(enum.Enum):
        DRIVE = "DRIVE"
        MOVE_TURRET = "MOVE_TURRET"

    def __init__(self, l_wheel, r_wheel, turret):
        super(Controller, self).__init__()

        # Components
        self.l_wheel = l_wheel
        self.r_wheel = r_wheel
        self.turret = turret

        self.components = {
            "l_wheel": l_wheel,
            "r_wheel": r_wheel,
            "turret": turret,
        }

        self.watch = WatchLoop()
        self.watch.set_callback(Controller.MethodEnum.DRIVE, self.stop_drive)
        self.watch.set_callback(Controller.MethodEnum.MOVE_TURRET, self.stop_turret)

    def initialize(self):
        super(Controller, self).initialize()

        for c in self.components.values():
            c.initialize()

    def is_initialized(self):
        # returns True only when all components are initialized
        return functools.reduce(lambda x, y: x and y, self.components.values(), True)

    def cleanup(self):
        GPIO.cleanup()

    def stop_all(self):
        print("stop all")
        for c in self.components.values():
            c.stop()

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

    def move_turret(self, rotate, updown):
        self.turret.rotate(rotate)
        self.turret.updown(updown)

        self.watch.record(Controller.MethodEnum.MOVE_TURRET)

    def stop_turret(self):
        self.turret.stop()


def _main():
    import concurrent.futures

    l_wheel = Wheel(1,2,None)
    r_wheel = Wheel(3,4,None)
    turret = Turret(5,6,7,8)
    con = Controller(l_wheel, r_wheel, turret)
    con.initialize()

    assert(con.is_initialized())

    executor = concurrent.futures.ThreadPoolExecutor()
    executor.submit(con.watch_loop)

    print("go")
    con.drive(1, 1)
    con.turret.rotate(1)
    GPIO.cleanup()


if __name__ == '__main__':
    _main()
