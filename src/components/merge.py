import core.make as make
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import components

"""
component reduction functions.  
2 args: reduced value and next value.

"""

def _symbol(s):
  try:
    return globals()[s]
  except:
    return False


def kind(p=[], n=[]):
  if not isinstance(p, list):
    p = []
  if not isinstance(n, list):
    n = []
  return list(set(p + n))
