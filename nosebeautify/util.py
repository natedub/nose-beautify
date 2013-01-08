def monkeypatch_method(cls):
    """MonkeyPatching decorator.

    Described by Guido van Rossum, here:
        http://mail.python.org/pipermail/python-dev/2008-January/076194.html

    This version keeps a reference to the original function in an 'orig'
    attribute on the new function object.
    """
    def decorator(func):
        orig = getattr(cls, func.__name__)
        setattr(cls, func.__name__, func)
        func.orig = orig
        return func
    return decorator

# Alternate idea for monkeypatching... this would allow us to enable
# the monkeypatches on demand, and revert afterwards.

class MonkeyPatcher(object):

    def __init__(self):
        self._patches = []
        self.originals = {}

    def method(self, cls):
        def decorator(func):
            self._patches.append((cls, func.__name__, func))
            return func
        return decorator

    def register(self, obj, attr, value):
        self._patches.append((obj, attr, value))

    def enable(self):
        for obj, attr, value in self._patches:
            orig = getattr(obj, attr)
            setattr(obj, attr, value)
            try:
                value.orig = orig
            except AttributeError:
                pass
            self.originals[(obj, attr)] = orig

    def disable(self):
        for obj, attr, value in self._patches:
            orig = self.originals[(obj, attr)]
            setattr(obj, attr, orig)
