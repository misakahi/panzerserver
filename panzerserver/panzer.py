import time
import threading
import enum
import functools

try:
    from RPi import GPIO
except ImportError:
    import fake_rpi
    from fake_rpi.RPi import GPIO


    def toggle_fake_print(p):
        fake_rpi.toggle_print(p)


class DriveDirection(enum.Enum):
    STOP = 0
    FORWARD = 1
    BACKWARD = 2
    BRAKE = 3


class Wheel(object):

    def __init__(self, channel1, channel2, channel_pwm=None):
        self.channel1 = channel1
        self.channel2 = channel2
        self.channel_pwm = channel_pwm

    def initialize(self):
        GPIO.setup(self.channel1, GPIO.OUT)
        GPIO.setup(self.channel2, GPIO.OUT)

    def forward(self, level):
        GPIO.output(self.channel1, GPIO.HIGH)
        GPIO.output(self.channel2, GPIO.LOW)

    def backward(self, level):
        GPIO.output(self.channel1, GPIO.LOW)
        GPIO.output(self.channel2, GPIO.HIGH)

    def brake(self, level):
        GPIO.output(self.channel1, GPIO.HIGH)
        GPIO.output(self.channel2, GPIO.HIGH)

    def stop(self):
        GPIO.output(self.channel1, GPIO.LOW)
        GPIO.output(self.channel2, GPIO.LOW)

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

    def __init__(self,
                 l_channel1, l_channel2, l_pwm,
                 r_channel1, r_channel2, r_pwm,
                 ):
        # Components
        self.l_wheel = Wheel(l_channel1, l_channel2, l_pwm)
        self.r_wheel = Wheel(r_channel1, r_channel2, r_pwm)

        self.last_updated = 0

    def initialize(self):
        self.l_wheel.initialize()
        self.r_wheel.initialize()

    def stop_all(self):
        print("stop all")
        self.l_wheel.stop()
        self.r_wheel.stop()

        self.touch()

    def touch(self):
        """Update last updated time
        :return:
        """
        self.last_updated = time.time()

    @classmethod
    def watch_configure(cls, interval, threshold):
        cls.WATCH_INTERVAL = interval
        cls.WATCH_THRESHOLD = threshold

    def watch_loop(self):
        self.touch()
        is_active = True
        while True:
            delta = (time.time() - self.last_updated) * 1e3  # milliseconds
            if is_active and delta > self.WATCH_THRESHOLD:
                self.stop_all()
                is_active = False
            elif delta <= self.WATCH_INTERVAL:
                is_active = True
            time.sleep(self.WATCH_INTERVAL / 1e3)  # seconds

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

        self.touch()


if __name__ == '__main__':
    import concurrent.futures

    con = Controller(
        1, 2, None, 3, 4, None
    )
    con.initialize()

    executor = concurrent.futures.ThreadPoolExecutor()
    executor.submit(con.watch_loop)

    print("go")
    con.drive(1, 1)
