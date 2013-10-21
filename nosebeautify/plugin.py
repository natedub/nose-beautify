import os
import logging

from nose.plugins import Plugin

from nosebeautify import color
from nosebeautify import monkeypatches

log = logging.getLogger(__name__)


class BeautifyPlugin(Plugin):

    name = 'beautify'

    # Run this plugin late to avoid our setOutputStream method
    # clobbering other plugin's stream handling.
    score = 10

    def addOptions(self, parser, env=os.environ):
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
        monkeypatches.patcher.enable()

    def finalize(self, result):
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

    def error_heading(string):
        error_flavor, description = string.split(':', 1)
        return ''.join([
            color.magenta(error_flavor), ':', color.white(description),
        ])

    startswith = [
        ('FAIL: ', error_heading),
        ('ERROR: ', error_heading),
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
        colorized = self.colorize(string)
        self.stream.write(colorized)

    def writeln(self, string=None):
        if string:
            self.write(string)
        self.stream.write('\n')
