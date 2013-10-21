import collections
import functools


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
        self._classes = collections.defaultdict(dict)
        self._originals = {}

    def method(self, cls):
        def decorator(func):
            name = func.__name__
            self._patches.append((cls, name, func))
            # TODO: This ought to be loaded on enable()
            self._classes[cls][name] = getattr(cls, name)
            return func
        return decorator

    def register(self, obj, attr, value):
        self._patches.append((obj, attr, value))

    def original(self, obj):
        class_ = obj.__class__
        methods = self._classes[class_]
        return _MonkeyProxy(obj, methods)

    def enable(self):
        for obj, attr, value in self._patches:
            orig = getattr(obj, attr)
            setattr(obj, attr, value)
            self._originals[(obj, attr)] = orig

    def disable(self):
        for obj, attr, value in self._patches:
            orig = self._originals[(obj, attr)]
            setattr(obj, attr, orig)


class _MonkeyProxy(object):
    def __init__(self, obj, methods):
        self._obj = obj
        self._methods = methods

    def __getattr__(self, attr):
        try:
            method = self._methods[attr]
        except KeyError:
            import ipdb; ipdb.set_trace()
            raise AttributeError(attr)
        return functools.partial(method, self._obj)
