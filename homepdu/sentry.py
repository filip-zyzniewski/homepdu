import snimpy


class Outlet(object):
    "Represents a single Sentry output."
    _states = {
        True: 'on',
        False: 'off',
    }

    def __init__(self, manager, index):
        self.manager = manager
        self.index = index
        self.id = self.manager.outletID[index]
        self.name = self.manager.outletName.get(index, id)

    def state(self):
        "Determines whether the output is on."
        return bool(self.manager.outletStatus[self.index])

    def on(self):
        "Turns the output on."
        self.set(True)

    def off(self):
        "Turns the output off."
        self.set(False)

    def set(self, state):
        """"Sets the desired output state.

        Accepts a boolean or an 'on'/'off'/'reboot' string."""
        state = self._states.get(state, state)
        self.manager.outletControlAction[self.index] = state

    def reboot(self):
        self.set('reboot')


class Sentry(dict):
    "Represents a Server Technology Sentry PDU unit."

    _defaults = {
        'version': 3,
        'authprotocol': 'MD5',
        'privprotocol': 'DES',
    }

    def __init__(self, *args, **kwargs):
        for mib in kwargs.pop('mibs', []):
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
        "Reloats the outlet information from the unit."
        self.clear()
        for index in self.manager.outletID:
            outlet = Outlet(self.manager, index)
            self[outlet.name] = outlet
