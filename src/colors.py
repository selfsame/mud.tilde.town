"""
ANSI Color Helpers
"""
import re
import string


ANSI_ESCAPE = '\x1b[{}m'
ANSI_RE = re.compile('\x1b\[((?:\d|;)*)m')
GROUPED_ANSI_RE = re.compile('((?:\x1b\[(?:\d|;)*m\s*)+)')
WHITESPACE_RE = re.compile('\s+')

COLORS = ('black', 'red', 'green', 'yellow', 'blue',
          'magenta', 'cyan', 'white')

special = {'face': '\02', 'heart': '\03', 'right': '\020',
           'down': '\037', 'up': '\036'}


def ansi(code):
    "Given a code num produce a ansi escape"
    if isinstance(code, (tuple, list, set)):
        code = ';'.join(code)
    return ANSI_ESCAPE.format(code)


CODES = {'resetall': ansi(0),
         'bold': ansi(1),
         'underline': ansi(4),
         'blink': ansi(5),
         'reverse': ansi(7),
         'boldoff': ansi(22),
         'blinkoff': ansi(25),
         'underlineoff': ansi(24),
         'reverseoff': ansi(27),
         'reset': ansi(39),
         'RESET': ansi(49)}

# fill in colors
for index, name in enumerate(COLORS):
    CODES[name] = ansi(index + 30)
    CODES[name.upper()] = ansi(index + 40)


def unstyle(text):
    """Remove all ANSI styling"""
    return ANSI_RE.sub('', text)


def _compress_ansi(matchobj):
    matched = matchobj.group(0)
    # We don't want to loose the whitespace between codes
    ws = WHITESPACE_RE.findall(matched)
    codes = ANSI_RE.findall(matched)
    return ansi(codes) + ''.join(ws)


def style(text, reset=True):
    """
    Text can contain color codes $CODE
    ALL CAP COLOR NAME = Background Color
    Templates can contain {} to prevent ambiguity

    The man with the red ${red}hat.

    Unknown codes are left in the styled text
    :param text: Text to style
    :param reset: Add resetall to end of string
    :return: styled text
    """
    if reset:
        text += '$resetall'
    styled = string.Template(text).safe_substitute(CODES)
    return GROUPED_ANSI_RE.sub(_compress_ansi, styled)


def color(name):
    return CODES[name]


def background(name):
    return CODES[name.upper()]


def wrap(s, c):
    return c+s+CODES['resetall']

