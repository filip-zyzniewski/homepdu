'Provides a reference counting event filter.'
import collections
import logging

Ref = collections.namedtuple('Ref', ['name', 'by', 'used'])
Ref.replace = Ref._replace


def ref_counter(source):
    """Processes usage information of named resources.

    Args:
        source: iterable of Ref tuples indicating whether named
                resource users use them or not.
    Yields:
        Ref tuples with by=None, indicating whether the resource
        is in use or not.
    """
    uses = collections.defaultdict(set)
    for ref in source:
        out = False
        use = uses[ref.name]
        if ref.used:
            out = not use
            use.add(ref.by)
        else:
            use.discard(ref.by)
            out = not use
        logging.debug('resource %s used by: %s', ref.name, ','.join(sorted(use)))
        if out:
            yield ref.replace(by=None)
