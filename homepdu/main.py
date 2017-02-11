import homepdu.sentry
import snimpy.manager

# ftp://ftp.servertech.com/Pub/SNMP/sentry3/Sentry3.mib
mibs = ['/usr/share/snmp/mibs/Sentry3-MIB.txt']

passwd = ''


def main():
    for m in mibs:
        snimpy.manager.load(m)

    sentry = homepdu.sentry.Sentry(
        host='pdu',
        secname='rw',
        password=passwd,
        mibs=mibs,
    )
    print(sentry.amplifier.state())
