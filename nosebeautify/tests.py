import logging

from unittest import TestCase
from unittest import TestSuite

from nose.plugins.logcapture import LogCapture
from nose.plugins import PluginTester

from nosebeautify.plugin import BeautifyPlugin

log = logging.getLogger(__name__)

logging.basicConfig(level=logging.DEBUG)

import sys
try:
    import ipdb as pdb
except ImportError:
    import pdb
def pdb_excepthook(type, value, traceback):
    pdb.post_mortem(traceback)
sys.excepthook = pdb_excepthook

class TestBeautifyPlugin(PluginTester, TestCase):
    activate = '--beautify'
    plugins = [BeautifyPlugin(), LogCapture()]

    def test_simple_colorizers(self):
        print self.output
        self.fail()

    def makeSuite(self):
        class TC(TestCase):
            def runTest(self):
                log.info('Die in a fire')
                raise ValueError('I hate foo')
        return TestSuite([TC()])
