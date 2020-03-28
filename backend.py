from threading import Event, Thread, enumerate
import time


class DaemonRoutine:
    def __init__(self, interval, func, *args, t_name=None):
        self.interval = interval
        self._func = func
        self._args = args
        self._stopped = Event()
        self.value = None
        self._t = Thread(target=self._loop, daemon=True, name=t_name)
        self._t.start()

    @property
    def is_running(self):
        return self._t.is_alive()

    def _loop(self):
        while not self._stopped.wait(self.interval):
            self.value = self._func(*self._args)

    def stop(self):
        self._stopped.set()

    def set_arg(self, *args):
        self._args = args




#def fetch_deamon_value(instance):