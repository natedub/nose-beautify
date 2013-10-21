from fancyformatter import FancyFormatter
from nose.plugins.capture import Capture
from nose.plugins.failuredetail import FailureDetail
from nose.plugins.logcapture import LogCapture
from nose.result import TextTestResult
from nose.util import safe_str
from pygments import highlight
from pygments.formatters import TerminalFormatter
from pygments.lexers import PythonTracebackLexer

from nosebeautify import color
from nosebeautify import util


patcher = util.MonkeyPatcher()

_formatter = None

def set_formatter(formatter):
    global _formatter
    _formatter = formatter


@patcher.method(FailureDetail)
def formatFailure(self, test, err):
    """Add detail from traceback inspection to error message of a failure.
    """
    ec, exc_text, tb = patcher.original(self).formatFailure(test, err)
    exc_text = format.highlight_tb(exc_text)
    return (ec, exc_text, tb)


@patcher.method(LogCapture)
def setupLoghandler(self):
    patcher.original(self).setupLoghandler()
    if _formatter:
        formatter = _formatter
    else:
        formatter = FancyFormatter(self.logformat, self.logdatefmt)
    self.handler.setFormatter(formatter)


@patcher.method(Capture)
@patcher.method(LogCapture)
def addCaptureToErr(self, ev, records):
    result = patcher.original(self).addCaptureToErr(ev, records)
    ev = safe_str(ev)
    added_lines = result[len(ev):].split('\n')
    added_lines[1] = color.green(added_lines[1], bold=True)
    added_lines[-1] = color.green(added_lines[-1], bold=True)
    return ev + '\n'.join(added_lines)


python_traceback_lexer = PythonTracebackLexer()
terminal_formatter = TerminalFormatter()


@patcher.method(TextTestResult)
def _exc_info_to_string(self, err, test=None):
    exc_text = super(TextTestResult, self)._exc_info_to_string(err, test)
    exc_text = highlight(exc_text, python_traceback_lexer, terminal_formatter)
    return exc_text
