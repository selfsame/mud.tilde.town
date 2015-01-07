from random import randint
import re

def is_number(n):
  return isinstance(n, (int, long, float))
  
def _roll(count, sides, plus = 0):
  res = 0
  for i in range(count):
    res += randint(1, sides)
  return res + plus

def is_dice(thing):
  if isinstance(thing, (str, unicode)):
    p = parse(thing)
    if p:
      return True
  return False

def parse(s):
  m = re.match(r"(?P<count>\d+)(d(?P<sides>\d+))*(\+(?P<plus>\d+))*", s)
  if m:
    res = {}
    md = m.groupdict()
    for k in md:
      if isinstance(md[k], (str, unicode)):
        res[k] = int(md[k])
      else:
        res[k] = 0
    return res
  return false

def roll(d):
  if isinstance(d, (str, unicode)):
    parsed = parse(d)
    if parsed:
      if parsed["sides"] == 0:
        return parsed["count"]
      else:
        return _roll(parsed["count"], parsed["sides"], parsed["plus"])
    else:
      return 0
  elif is_number(d):
    return d
  else:
    return 0

def table_choice(t):
  total = 0
  lookup = []
  for k in t:
    if is_number(t[k]):
      total += t[k]
      lookup.append([total, k])
  r = randint(0,total)
  for lv in lookup:
    if r <= lv[0]:
      return lv[1]



def test():
  print roll(5)
  print roll("1d12")
  print roll("3d4+12")
  print roll("45")
  table = {"cat":20, "mouse":5, "dog":30, "cockroach": 1}
  for i in range(10):
    print table_choice(table)
