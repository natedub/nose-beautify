import os
import logging

from nose.plugins import Plugin

import sys
try:
    import ipdb as pdb
except ImportError:
    import pdb
def pdb_excepthook(type, value, traceback):
    pdb.post_mortem(traceback)
sys.excepthook = pdb_excepthook

from nosebeautify import color
from nosebeautify import monkeypatches

log = logging.getLogger(__name__)

class BeautifyPlugin(Plugin):

    name = 'beautify'
    score = 10 ** 5

    def add_options(self, parser, env=os.environ):
        """Add command-line options for this plugin"""
        parser.add_option('--beautify',
                          dest='beautify',
                          action='store_true',
                          default=env.get('NOSE_BEAUTIFY', False),
                          help='Display color results, tracebacks, and SQL queries.')

    def configure(self, options, conf):
        if options.beautify:
            self.enabled = True

    def setOutputStream(self, stream):
        return ColorizingStream(stream)

    def begin(self):
        return
        monkeypatches.patcher.enable()

    def finalize(self, result):
        return
        monkeypatches.patcher.disable()

class ColorizingStream(object):
    def __init__(self, stream):
        self.stream = stream

    def __getattr__(self, attr):
        # unittest.result._WritelnDecorator checks 'stream' here too, but
        # getattr is never invoked when that name is accessed.
        if attr == '__getstate__':
            raise AttributeError(attr)
        return getattr(self.stream, attr)

    simple_colorizers = {
        'ok': color.green,
        'E': color.red,
        'ERROR': color.red,
        'F': color.red,
        'FAILURE': color.red,
        'FAILED': color.red,
        '=' * 70: color.white,
        '-' * 70: color.white,
        ' ... ': color.green,
        'expected failure': color.white,
        'unexpected success': color.white,
    }

    startswith = [
        ('skipped ', None),
        ('FAIL: ', None),
        ('ERROR: ', None),
    ]

    def colorize(self, string):
        if string in self.simple_colorizers:
            colorizer = self.simple_colorizers[string]
            return colorizer(string)

        for prefix, colorizer in self.startswith:
            if string.startswith(prefix):
                return colorizer(string)

        return string

    def write(self, string):
        print type(string), string
        colorized = self.colorize(string)
        self.stream.write(colorized)
