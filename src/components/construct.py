import core.make as make
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import parse
import data
import random
import components

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

def contents(d):
  #we need a new list, as d is a reference
  res = []
  for e in d:
    if e.get("id"):
      c_e = components.construct(e)
      new = components.instance(e.get("id"))
      #we merge the conent entry onto the instance
      merged = dict(new.items() + c_e.items())
      components.register(merged)
      res.append(merged.get("uuid"))
  return res

def exits(d):
  res = {}
  for ustr in d:
    dtype = data.datatypes.get(d[ustr])
    if dtype:
      res[ustr] = d[ustr]
  return d

def inventory(d):
  return {"contents":[]}

def acting(d):
  d["ap"] = random.randint(20,50)
  return d

def spawning(d):
  res = {"rate":100, "max":5, "instances":[]}
  res = dict(res.items() + d.items())
  res["timer"] = 0
  return res
