import logging

import snimpy.manager

import homepdu.dev
import homepdu.sysfs
import homepdu.sentry
import homepdu.funnel
import homepdu.refcnt

passwd = ''


dpms = '/sys/class/drm/card0-DVI-D-1/dpms'
sound = '/dev/snd/pcmC0D0p'

def main():
    logging.getLogger().setLevel(logging.DEBUG)
    sentry = homepdu.sentry.Sentry(
        host='pdu',
        secname='rw',
        password=passwd,
    )

    events = homepdu.funnel.funnel(
        (
            homepdu.refcnt.Ref(
                name='amplifier',
                by=fn,
                used=used
            ) for fn, used in
            homepdu.dev.watch(sound)
        ),
        (
            homepdu.refcnt.Ref(
                name='screen',
                by=dpms,
                used=state.lower() == 'on'
            ) for state in
            homepdu.sysfs.poll(dpms)
        )
    )

    for ref in homepdu.refcnt.RefCounter(events):
        sentry[ref.name].set(ref.used)
