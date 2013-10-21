import logging
import unittest

log = logging.getLogger(__name__)

class TestFailure(unittest.TestCase):
    def test_pass(self):
        pass

    def test_fail(self):
        log.info('Example log message')
        print 'Example stdio'
        self.fail('This failure is intentional')
