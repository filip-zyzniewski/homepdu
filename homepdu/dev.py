'Provides usage info based on open/close operations on device files.'

import logging
import pyinotify

class _EventHandler(pyinotify.ProcessEvent):
    # pylint: disable=invalid-name

    mask = (
        # pylint: disable=no-member
        pyinotify.IN_OPEN |
        pyinotify.IN_CLOSE_WRITE |
        pyinotify.IN_CLOSE_NOWRITE
    )

    def __init__(self):
        self.usage = {}
        super(_EventHandler, self).__init__()

    def process_IN_OPEN(self, event):
        'Handler for the IN_OPEN event.'
        logging.debug('accessed: %s', event.pathname)
        self.usage[event.pathname] = True

    def process_IN_CLOSE_WRITE(self, event):
        'Handler for the IN_CLOSE_WRITE event.'
        logging.debug('closed: %s', event.pathname)
        self.usage[event.pathname] = False

    process_IN_CLOSE_NOWRITE = process_IN_CLOSE_WRITE

    def events(self):
        """Flushes registered events.

        Yields:
            (path, used) pairs (see watch).
        """
        while self.usage:
            yield self.usage.popitem()


def watch(*paths):
    """Reports usage of passed device files.

    Args:
        paths: names of the files to watch

    Yields:
        (path, used) pairs, where used is True for a file that has
        been opened and False for a file that has been closed.
    """
    manager = pyinotify.WatchManager()
    handler = _EventHandler()
    notifier = pyinotify.Notifier(manager, handler)

    logging.info('watching: %s', ', '.join(paths))
    manager.add_watch(list(paths), handler.mask)

    while True:
        notifier.process_events()
        for event in handler.events():
            yield event
        if notifier.check_events():
            notifier.read_events()
