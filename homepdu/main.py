import logging

import snimpy.manager

import homepdu.dpms
import homepdu.sentry
import homepdu.sink

passwd = ''


def main():
    logging.getLogger().setLevel(logging.INFO)
    sentry = homepdu.sentry.Sentry(
        host='pdu',
        secname='rw',
        password=passwd,
    )

    dpms = (
        lambda: sentry.screen.set(s) for s in
        homepdu.dpms.poll('card0-DVI-D-1')
    )

    for c in homepdu.sink.sink(dpms):
        c()
