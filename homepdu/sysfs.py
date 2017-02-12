import logging
import time


def poll(fn, interval=1):
    """Detects changes in a sysfs file.

    Args:
        fn: either aabsolute path to a sysfs file,
        e.g. /sys/class/drm/card0-VGA-1/dpms.
        interval: how many seconds to wait between pols.
    Yields:
        str, contents of the file, when it changes.
    """

    old = None
    with open(fn) as f:
        logging.info('polling contents of %s every %s seconds', fn, interval)
        while True:
            f.seek(0)
            state = f.read().strip()
            if state != old:
                logging.info('%s went from %s to %s', fn, old, state)
                yield state
            old = state
            time.sleep(interval)
