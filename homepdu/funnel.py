'Provides a funciton draining multiple iterables in separate threads.'

import threading
import queue


def _drain(iterable, que):
    for i in iterable:
        que.put(i)


class _ThreadManager(object):
    # pylint: disable=too-few-public-methods

    def __init__(self, *threads):
        self.threads = threads

    def __enter__(self):
        for thread in self.threads:
            thread.start()

    def __exit__(self, *exc):
        for thread in self.threads:
            thread.join()


def funnel(*iterables):
    """Drains iterables in separate threads and funnels their outputs together.

    Args:
        iterables: iterables to drain

    Yields:
        items yielded by iterables, FIFO.
    """

    que = queue.Queue(maxsize=1)
    threads = [
        threading.Thread(target=_drain, args=(i, que))
        for i in iterables
    ]

    with _ThreadManager(*threads):
        while True:
            yield que.get()
