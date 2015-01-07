import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from util import contents_of, from_uid
import components
"""
component functions to transform their data for json serialization. (probably)
"""

def _symbol(s):
  try:
    return globals()[s]
  except:
    return False

def player(d):
	return True

def contents(d):
	conts = map(from_uid, d)
	return map(components.serialize, conts)
