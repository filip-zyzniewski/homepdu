'Provides the entry point of the homepdu service.'
import logging
import os

import homepdu.dev
import homepdu.sysfs
import homepdu.sentry
import homepdu.funnel
import homepdu.refcnt

PASSWD = ''

def dpms(output, outlet):
    """A generator controlling display power for a given video output.

    Args:
        output: name of the video output
                (must exist in /sys/class/drm, e.g. card0-VGA-1).
        outlet: name of the PDU outlet.

    Yields:
        homepdu.refcnt.Ref, usage information
    """
    path = os.path.join('/sys/class/drm', output, 'dpms')
    return (
        homepdu.refcnt.Ref(
            name=outlet,
            by=path,
            used=state.lower() == 'on'
        ) for state in
        homepdu.sysfs.poll(path)
    )


def alsa(card, device, outlet):
    """A generator controlling amplifier power for a given alsa device.

    Args:
        card: Alsa card number (see /proc/asound/cards).
        device: Alsa device number (see /proc/asound/devices).
        outlet: name of the PDU outlet.

    Yields:
        homepdu.refcnt.Ref, usage information
    """
    path = '/dev/snd/pcmC%dD%dp' % (card, device)
    return (
        homepdu.refcnt.Ref(name=outlet, by=upath, used=used)
        for upath, used in homepdu.dev.watch(path)
    )


def main():
    'Entry point of the homepdu service.'
    logging.getLogger().setLevel(logging.DEBUG)
    sentry = homepdu.sentry.Sentry(
        host='pdu',
        secname='rw',
        password=PASSWD,
    )

    events = homepdu.funnel.funnel(
        alsa(0, 0, 'amplifier'),
        dpms('card0-DVI-D-1', 'screen')
    )

    for ref in homepdu.refcnt.ref_counter(events):
        sentry[ref.name].set(ref.used)
