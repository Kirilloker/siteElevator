import time


class Timer:
    def __init__(self, delay, manager):
        self.delay = delay
        self.manager = manager

    def delayBeforeClose(self):
        time.sleep(self.delay)
        self.manager.closeDoor()
