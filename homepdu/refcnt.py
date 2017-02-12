import collections
import logging

Ref = collections.namedtuple('Ref', ['name', 'by', 'used'])
Ref.replace = Ref._replace

def RefCounter(source):
    uses = collections.defaultdict(set)
    for ref in source:
        y = False
        s = uses[ref.name]
        if ref.used:
            y = not s
            s.add(ref.by)
        else:
            s.discard(ref.by)
            y = not s
        logging.debug(
            'resource %s used by: %s' %
            (ref.name, ','.join(sorted(s)))
        )
        if y:
            yield ref.replace(by=None)
