from nose.plugins.failuredetail import FailureDetail
from nose.plugins.logcapture import LogCapture
from nose.result import TextTestResult

from nosebeautify import logs
from nosebeautify import util
from nosebeautify import format

patcher = util.MonkeyPatcher()

@patcher.method(FailureDetail)
def formatFailure(self, test, err):
    """Add detail from traceback inspection to error message of a failure.
    """
    orig_method = patcher.originals[(FailureDetail, 'formatFailure')]
    ec, exc_text, tb = orig_method(self, test, err)
    exc_text = format.highlight_tb(exc_text)
    return (ec, exc_text, tb)

@patcher.method(LogCapture)
def setupLoghandler(self):
    original_method = patcher.originals[(LogCapture, 'setupLoghandler')]
    original_method(self)
    formatter = logs.ColorizingFormatter(self.logformat, self.logdatefmt)
    self.handler.setFormatter(formatter)

@patcher.method(TextTestResult)
def _exc_info_to_string(self, err, test=None):
    exc_text = super(TextTestResult, self)._exc_info_to_string(err, test)
    exc_text = format.highlight_tb(exc_text)
    return exc_text

patcher.enable()
