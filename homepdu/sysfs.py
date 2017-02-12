'Provides periodic polling of a sysfs file.'

import logging
import time


def poll(path, interval=1):
    """Detects changes in a sysfs file.

    Args:
        path: either aabsolute path to a sysfs file,
              e.g. /sys/class/drm/card0-VGA-1/dpms.
        interval: how many seconds to wait between pols.
    Yields:
        str, contents of the file, when it changes.
    """

    old = None
    with open(path) as file:
        logging.info('polling contents of %s every %s seconds', path, interval)
        while True:
            file.seek(0)
            state = file.read().strip()
            if state != old:
                logging.info('%s went from %s to %s', path, old, state)
                yield state
            old = state
            time.sleep(interval)
