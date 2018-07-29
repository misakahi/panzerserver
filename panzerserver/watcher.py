import time


class TimeRecorder(object):

    def __init__(self):
        self._record = dict()

    def record(self, tag):
        t = time.time()
        self._record[tag] = t

    def get(self, tag):
        return self._record.get(tag, -1)

    def get_record(self):
        return self._record.copy()


class WatchLoop(object):

    def __init__(self, threshold_msec=200, interval_msec=None):
        self._callbacks = dict()
        self._recorder = TimeRecorder()
        self._is_active = False
        self._threshold = 0
        self._interval = 0
        self.set_thresold(threshold_msec, interval_msec)

    def set_callback(self, tag, callback):
        self._callbacks[tag] = callback

    def set_thresold(self, threshold_msec, interval_msec=None):
        self._threshold = threshold_msec / 1e3  # sec
        self._interval = self._threshold / 3 if interval_msec is None else interval_msec / 1e3  # sec

    @staticmethod
    def _do_nothing():
        pass

    def run_callback(self, tag):
        callback = self._callbacks.get(tag, WatchLoop._do_nothing)
        callback()

    def record(self, tag):
        self._recorder.record(tag)

    def get_record(self):
        return self._recorder.get_record()

    def start(self):
        # set initial records
        for tag in self._callbacks.keys():
            self.record(tag)
        self._is_active = True

        # flag whether to run callback
        is_callback_active = {tag: True for tag in self.get_record().keys()}
        while self._is_active:
            current_time = time.time()
            for tag, last_updated in self.get_record().items():
                delta = current_time - last_updated

                # Check elapsed from last updated. Run callback only when flag is true,
                # otherwise callback runs every time.
                if is_callback_active[tag] and delta > self._threshold:
                    print("watch callback delta={} threshold={} tag={}".format(delta, self._threshold, tag))
                    self.run_callback(tag)
                    is_callback_active[tag] = False
                elif delta <= self._threshold:
                    is_callback_active[tag] = True
            time.sleep(self._interval)

    def stop(self):
        self._is_active = False


def _test():
    import concurrent.futures

    watch = WatchLoop(100)
    watch.set_callback("test1", lambda: print("test1 callback"))
    watch.set_callback("test2", lambda: print("test2 callback"))

    executor = concurrent.futures.ThreadPoolExecutor()
    executor.submit(watch.start)
    for i in range(10):
        print("test1 %d" % i)
        watch.record("test1")
        if i % 2 == 0:
            print("test2 %d" % i)
            watch.record("test2")
        time.sleep(0.09)
    watch.stop()


if __name__ == '__main__':
    _test()
