'Representation of a Server Technology Sentry PDU.'

import logging

import snimpy.manager


class Outlet(object):
    'Represents a single Sentry outlet.'
    _states = {
        True: 'on',
        False: 'off',
    }

    def __init__(self, manager, index):
        self.manager = manager
        self.index = index
        self.oid = self.manager.outletID[index]
        self.name = self.manager.outletName.get(index, self.oid)

    def state(self):
        """Determines whether the outlet is on.

        Returns: bool - True means on, False means off.
        """
        return bool(self.manager.outletStatus[self.index])

    def on(self):  # pylint: disable=invalid-name
        'Turns the outlet on.'
        self.set(True)

    def off(self):
        'Turns the outlet off.'
        self.set(False)

    def set(self, state):
        """Applies the desired outlet state.

        Args:
            state: True/'on'/False,'off','reboot'
        """
        state = self._states.get(state, state)
        logging.info('setting %s to %s', self.name, state)
        self.manager.outletControlAction[self.index] = state

    def reboot(self):
        'Reboots the outlet.'
        self.set('reboot')


class Sentry(dict):
    'Represents a Server Technology Sentry PDU.'

    _defaults = {
        'version': 3,
        'authprotocol': 'MD5',
        'privprotocol': 'DES',
    }

    # ftp://ftp.servertech.com/Pub/SNMP/sentry3/Sentry3.mib
    _mibs = ['/usr/share/snmp/mibs/Sentry3-MIB.txt']

    def __init__(self, *args, **kwargs):
        super(Sentry, self).__init__()
        for mib in kwargs.pop('mibs', self._mibs):
            snimpy.manager.load(mib)
        kwargs = dict(self._defaults, **kwargs)
        password = kwargs.pop('password', None)
        if password:
            kwargs['authpassword'] = password
            kwargs['privpassword'] = password
        self.manager = snimpy.manager.Manager(*args, **kwargs)
        self.reload()

    __getattr__ = dict.__getitem__

    def reload(self):
        'Reloats the outlet information from the unit.'
        self.clear()
        for index in self.manager.outletID:
            outlet = Outlet(self.manager, index)
            self[outlet.name] = outlet
        logging.info(
            'found %d outlets: %s',
            len(self),
            ', '.join(sorted(self.keys()))
        )
