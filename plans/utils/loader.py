# -*- coding: utf-8 -*-


def load_class(name):
    """
    load a class by dotted path.
    """
    parts = name.split('.')
    module = __import__('.'.join(parts[0:-1]), globals(), locals(), [parts[-1]])
    return getattr(module, parts[-1])
