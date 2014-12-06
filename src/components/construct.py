import make
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import parse
import data

"""
component constructor functions.  
1 arg: datatype component value, return the instanced component value.

"""

def _symbol(s):
  try:
    return globals()[s]
  except:
    return False

def extends(d):
    res = {}
    for ustr in d:
        res = dict(res.items() + make.instance(ustr).items())
    return res

def living(d):
    hpmax = d['hpmax']
    if parse.dice.is_dice(d['hpmax']):
        hpmax = parse.dice.roll(d['hpmax'])
    d['hp'] = hpmax
    d['hpmax'] = hpmax
    return d

def room(d):
  return {"contents":[]}

def exits(d):
  res = {}
  for ustr in d:
    dtype = data.datatypes.get(d[ustr])
    if dtype:
      res[ustr] = d[ustr]
  print res
  return d

