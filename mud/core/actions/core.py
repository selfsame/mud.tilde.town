import collections
from mud.core.util import fn_name, name, players_in_scope, contents_of, from_uid
from mud.core import data
from mud.core.data import registry
from mud.core.parse import template
import mud.core.components

__all__ = ["given", "check", "before", "after", "action", "act", "act_stack", "say", "report", "report_to"]

def OD(ltps=[]):
  return collections.OrderedDict(ltps)


def given(*types, **kw):
  try:
      def decorator(f):
          def newf(*args):
              return f(*args)
          newf.__name__ = f.__name__
          return {types:newf}
      return decorator
  except KeyError, key:
      raise KeyError, key + "is not a valid keyword argument"
  except TypeError, msg:
      raise TypeError, msg

def tunnel(cursor, key, notfound={}):
  if key not in cursor:
    cursor[key] = notfound
  return cursor[key]

def walk(cursor, key):
  if cursor:
    if cursor.get(key):
      return cursor[key]
  return False


def _register(f, tag, spec=[]):
    v = f.__name__
    arity = len(spec)
    cursor = tunnel(registry, v, OD())
    cursor = tunnel(cursor, arity, OD())
    cursor = tunnel(cursor, tag, OD())    
    cursor = tunnel(cursor, spec, f)



def before(f):
  for k in f:
    _register(f[k], "before", k)
  def f_w(a, b):
    return f[k](a, b)    
  return f

def after(f):
  for k in f:
    _register(f[k], "after", k)
  def f_w(a, b):
    return f[k](a, b)    
  return f

def instead(f):
  for k in f:
    _register(f[k], "instead", k)
  def f_w(a, b):
    return f[k](a, b)    
  return f

def check(f):
  for k in f:
    _register(f[k], "check", k)
  def f_w(a, b):
    return f[k](a, b)    
  return f

def action(f):
  for k in f:
    _register(f[k], "action", k)
  def f_w(a, b):
    return f[k](a, b)    
  return f



def printable_preds(col):
  return "<"+", ".join(map(fn_name, col))+">"

def compose(roles, args, report = []):
  for f in roles.get("check") or []:
    if not apply(f, args): 
      print "[check failed]"
      return False
  res = {}
  for role in ["before", "action", "after"]:
    fns = roles.get(role) or []
    for f in fns:
      try:
        res[role] = apply(f, args)
      except:
        print "ACTION ERROR: "+fn_name(f)+"["+role+"]"+"\r\n    "+"".join(report)
        return res
      break
  return res

def speccheck(t, e):
  return t(e)



def dict_act(verb, *args):
  arity = len(args)
  cursor = walk(registry, verb)
  cursor = walk(cursor, arity)
  if cursor:
    results = OD()
    report = []
    for role in cursor:
      rolereport = []
      for spec in cursor[role]:
        good = True
        specced = map(speccheck, spec, args)
        for b in specced:
          if b == False:
            good = b
            break
        if good:
          roledict = tunnel(results, role, [])
          roledict.insert(0, cursor[role][spec])
          rolereport +=  [str(printable_preds(spec))]
      if len(rolereport) > 0:
        report.append(" ".join(["  "+str(role)+"->["] + rolereport + ["]\r\n"]))
    res = compose(results, args, report)
    return res


def act(verb, *args):
  res = apply(dict_act, [verb] + list(args))
  if res:
    return res.get("action")

def act_stack(verb, *args):
  out = []
  res = apply(dict_act, [verb] + list(args))
  if res:   
    for role in ["before", "action", "after"]:
      if res.get(role):
        out.append(res.get(role))
  return out


def say(*args):
  if data.subject.get("player"):
    data.subject['player'].send(template("".join(args)))

def report(*args):
  data.reportstack.append(" ".join(args))

def report_to(room, *args):
  observers = map(from_uid, contents_of(room))
  for actor in observers:
    if actor.get("player"):
      if data.subject != actor:
        actor["player"].send(template(" ".join(args)))







