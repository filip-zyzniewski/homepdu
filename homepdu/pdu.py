class Pdu(object):
    def __init__(self):
        pass

    def on(self, output):
        self.set(output, True)

    def off(self, output):
        self.set(output, False)

    def set(self, output, value):
        pass

    def get(self, output):
        pass


    def outputs(self):
        return []

