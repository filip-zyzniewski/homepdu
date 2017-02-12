import logging
import pyinotify

import homepdu.refcnt



class _EventHandler(pyinotify.ProcessEvent):
    mask = (
        pyinotify.IN_OPEN |
        pyinotify.IN_CLOSE_WRITE |
        pyinotify.IN_CLOSE_NOWRITE
    )

    def __init__(self):
        self.usage = {}
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

    def events(self):
        while self.usage:
            yield self.usage.popitem()



def watch(*fns):
    wm = pyinotify.WatchManager()
    eh = _EventHandler()
    notifier = pyinotify.Notifier(wm, eh)

    logging.info('watching: %s', ', '.join(fns))
    wm.add_watch(list(fns), eh.mask)

    while True:
        notifier.process_events()
        for e in eh.events():
            yield e
        if notifier.check_events():
            notifier.read_events()

