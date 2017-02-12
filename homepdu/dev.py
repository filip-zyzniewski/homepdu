import logging
import pyinotify

import homepdu.refcnt

_events = pyinotify.IN_OPEN | pyinotify.IN_CLOSE_WRITE | pyinotify.IN_CLOSE_NOWRITE


class _EventHandler(pyinotify.ProcessEvent):
    def __init__(self, usage):
        self.usage = usage
        super(_EventHandler, self).__init__()

    def process_IN_OPEN(self, event):
        fn = event.pathname
        logging.debug('accessed: %s', fn)
        self.usage[fn] = True

    def process_IN_CLOSE_WRITE(self, event):
        fn = event.pathname
        logging.debug('closed: %s', fn)
        self.usage[fn] = False

    process_IN_CLOSE_NOWRITE = process_IN_CLOSE_WRITE


def watch(*fns):
    wm = pyinotify.WatchManager()
    usage = {}
    notifier = pyinotify.Notifier(wm, _EventHandler(usage))

    logging.info('watching: %s', ', '.join(fns))
    wm.add_watch(list(fns), _events)

    while True:
        notifier.process_events()
        while usage:
            yield usage.popitem()
        if notifier.check_events():
            notifier.read_events()

