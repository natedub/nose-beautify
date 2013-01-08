import logging

from pygments import highlight
from pygments.formatters import TerminalFormatter
from pygments.lexers import MySqlLexer
from pygments.lexers import PythonLexer
from pygments.lexers import PythonTracebackLexer

from nosebeautify import color


LEVELS = {
    'WARNING': color.red(' WARN', bold=True),
    'INFO': color.blue(' INFO'),
    'DEBUG': color.blue('DEBUG'),
    'CRITICAL': color.magenta(' CRIT'),
    'ERROR': color.red('ERROR'),
}

class ColorizingFormatter(logging.Formatter):
    pass

mysql_lexer = MySqlLexer()
python_lexer = PythonLexer()
python_traceback_lexer = PythonTracebackLexer()
terminal_formatter = TerminalFormatter()

def highlight_tb(exc_text):
    return highlight(exc_text, python_traceback_lexer, terminal_formatter)

def highlight_sql(text):
    return highlight(text, mysql_lexer, terminal_formatter)

def highlight_python(text):
    return highlight(text, python_lexer, terminal_formatter)
