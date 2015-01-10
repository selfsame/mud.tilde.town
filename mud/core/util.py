from mud.core import data
from CAPSMODE import *


def fn_name(f):
  try:
    return f.__name__
  except:
    return str(f)

def the(thing, compstr, default=False):
    if thing:
      if compstr in thing:
          return thing[compstr]
      else:
          return default

def name(thing):
  if isinstance(thing, dict):
    return FIRST(filter(INVERT(NONE), map(INF(GET, thing, "%1"), ['name','firstname','ustr','id'])))
  if thing == None:
    return "nothing"
  return str(type(thing))

def its(k, notfound = None):
  def _its_(e):
    if isinstance(e, dict):
      if e.get(k): return e[k]
    return notfound
  return _its_

def get_in(col, ks, notfound = None):
  for k in ks:
    if isinstance(col, dict):
      if k in col:
        col = col[k]
      else: return notfound
    else: return notfound
  return col

def fn_2(fn, arg2):
  def _fn_2(arg1):
    return fn(arg1, arg2)
  return _fn_2

def map_get_in(ks, col):
  return map(fn_2(get_in, ks), col)



def from_uid(s):
  if isinstance(s, str):
    r = data.rooms.get(s)
    if not r:
      r = data.instances.get(s)
    if r: return r
  elif isinstance(s, dict):
    return s
  print "NO FROM_UID FOR ", s

def contents_of(r):
  conts = r.get('contents')
  if r:
    return map(from_uid, conts)
  return []

def holder_of(e):
  conts = r.get('contents')
  if r:
    return map(from_uid, conts)
  return []

def location(e):
  r = the(e,"located")
  room = data.rooms.get(r)
  if room: return room
  return from_uid(r)

def path(e):
  l = e.get('located')
  if l: return [l]+ path(from_uid(l))
  return []


def players_in_scope(scope):
  res = []
  if not scope: return res
  for e in scope:
    actor = from_uid(e)
    if the(actor,"player"):
      res.append(actor)
  return res

def connected_rooms(r):
  exits = the(r,"exits")
  if not exits: return []
  res = []
  for k in exits:
    res.append(from_uid(exits[k]))
  return res


