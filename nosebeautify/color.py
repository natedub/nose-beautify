import re

from functools import partial


__all__ = [
    'blue',
    'cyan',
    'green',
    'magenta',
    'red',
    'strip',
    'white',
    'yellow',
]

def _colorcode(c, text, bold=False):
    if bold:
        c = '1;%s' % c
    return '\033[%sm%s\033[0m' % (c, text)

red = partial(_colorcode, 31)
green = partial(_colorcode, 32)
yellow = partial(_colorcode, 33)
blue = partial(_colorcode, 34)
magenta = partial(_colorcode, 35)
cyan = partial(_colorcode, 36)
white = partial(_colorcode, 37)

_re_color_codes = re.compile(r'\033\[(\d;)?\d+m')

def strip(text):
    """Remove all color codes from a string."""
    return _re_color_codes.sub('', text)
