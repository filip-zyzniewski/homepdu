import logging
import os
import select
import sys
import time


def poll(fn, interval=1):
    """Detects changes in DPMS state of a display output.

    Args:
        fn: either a basename of a directory under
        /sys/class/drm/ (e.g. 'card0-VGA-1') or an
        absolute path to the sysfs dpms state file,
        e.g. /sys/class/drm/card0-VGA-1/dpms.
        interval: how many seconds to wait between pols.
    Yields:
        booleans representing current DPMS state on changes.
    """

    old = None
    with open(_path(fn)) as f:
        while True:
            f.seek(0)
            state = f.read(3).strip().lower()
            if state != old:
                logging.info("%s went from %s to %s", fn, old, state)
                yield state == 'on'
            old = state
            time.sleep(interval)


def _path(name):
    if os.path.isabs(name):
        return name
    return os.path.join('/sys/class/drm', name, 'dpms')
