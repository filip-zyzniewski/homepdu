import threading
import queue


def _drain(iterable, queue):
    for i in iterable:
        queue.put(i)


class _ThreadManager(object):
    def __init__(self, *threads):
        self.threads = threads

    def __enter__(self):
        for thread in self.threads:
            thread.start()

    def __exit__(self, *exc):
        for thread in self.threads:
            thread.join()


def funnel(*iterables):
    """Drains iterables in separate threads and funnels their outputs.

    Args:
        *iterables: iterables to drain

    Yields:
        items yielded by iterables, FIFO.
    """

    q = queue.Queue(maxsize=1)
    threads = [threading.Thread(target=_drain, args=(i, q)) for i in iterables]

    with _ThreadManager(*threads):
        while True:
            yield q.get()
