import mttlang
import dice
import re
from dice import table_choice

def words(s):
  return re.findall('[\w]+', s)

def first_word(col):
  if isinstance(col, (str, unicode)):
    col = words(col)
  return "".join(col[0:1])

def strip_escape_chars(raw):
  if raw.startswith('\xff'):
    raw = raw[3:]
  sp = repr(raw).split('\\x08')
  word = ""
  active = 0
  for i in range( len(sp) - 1 ):
    if sp[i] == '':
      sp[active] = sp[active][:-1]
    else:
      sp[i] = sp[i][:-1]
      active = i
  for entry in sp:
    word += entry
  return word[1:-1]


def template(s):
  return mttlang.handlebars(s)
