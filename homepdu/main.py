'Provides the entry point of the homepdu service.'
import logging

import homepdu.dev
import homepdu.sysfs
import homepdu.sentry
import homepdu.funnel
import homepdu.refcnt

PASSWD = ''
DPMS = '/sys/class/drm/card0-DVI-D-1/dpms'
SOUND = '/dev/snd/pcmC0D0p'


def main():
    'Entry point of the homepdu service.'
    logging.getLogger().setLevel(logging.DEBUG)
    sentry = homepdu.sentry.Sentry(
        host='pdu',
        secname='rw',
        password=PASSWD,
    )

    events = homepdu.funnel.funnel(
        (
            homepdu.refcnt.Ref(
                name='amplifier',
                by=fn,
                used=used
            ) for fn, used in
            homepdu.dev.watch(SOUND)
        ),
        (
            homepdu.refcnt.Ref(
                name='screen',
                by=DPMS,
                used=state.lower() == 'on'
            ) for state in
            homepdu.sysfs.poll(DPMS)
        )
    )

    for ref in homepdu.refcnt.ref_counter(events):
        sentry[ref.name].set(ref.used)
