import time
import Manager


class Timer:
    def __init__(self, delay, manager : Manager):
        self.delay = delay
        self.manager = manager

    def delayBeforeClose(self):
        time.sleep(self.delay)
        self.manager.closeDoor()
