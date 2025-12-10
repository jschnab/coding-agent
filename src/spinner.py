import functools
import itertools
import sys
import threading
import time
from contextlib import contextmanager

from .terminal import reset_terminal_color


class Spinner:
    def __init__(self, message="Working", delay=0.1):
        self.spinner = itertools.cycle("|/-\\")
        self.delay = delay
        self.message = message
        self._running = False
        self._thread = None

    def _spin(self):
        reset_terminal_color()
        while self._running:
            frame = next(self.spinner)
            sys.stdout.write(f"\r{frame} {self.message}")
            sys.stdout.flush()
            time.sleep(self.delay)
        sys.stdout.write(f"\r\033[32m✔\033[0m {self.message}\n\n")
        sys.stdout.flush()

    def start(self):
        if self._running:
            return
        self._running = True
        self._thread = threading.Thread(target=self._spin)
        self._thread.daemon = True
        self._thread.start()

    def stop(self):
        self._running = False
        if self._thread is not None:
            self._thread.join()


def spin(message):
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            sp = Spinner(message)
            sp.start()
            try:
                return await func(*args, **kwargs)
            finally:
                sp.stop()

        return wrapper

    return decorator


@contextmanager
def spin_context(message):
    sp = Spinner(message)
    sp.start()
    try:
        yield sp
    finally:
        sp.stop()
