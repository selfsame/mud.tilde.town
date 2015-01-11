import collections
from mud.core.util import fn_name, name, players_in_scope, contents_of, from_uid
from mud.core import data
from mud.core.data import registry
from mud.core.parse import template
import mud.core.components
from mud.core import predicates

__all__ = ["given", "check", "before", "after", "instead", "fail", "call", "act_stack", "say", "report", "report_to"]

def OD(ltps=[]):
  return collections.OrderedDict(ltps)



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

def check(*types):
  def decorator(f):
    _register(f, "check", types)
    return f
  return decorator

def before(*types):
  def decorator(f):
    _register(f, "before", types)
    return f
  return decorator

def given(*types):
  def decorator(f):
    _register(f, "action", types)
    return f
  return decorator

def after(*types):
  def decorator(f):
    _register(f, "after", types)
    return f
  return decorator

def instead(*types):
  def decorator(f):
    _register(f, "instead", types)
    return f
  return decorator

def fail(*types):
  def decorator(f):
    _register(f, "fail", types)
    return f
  return decorator



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
      res[role] = apply(f, args)
      break
  return res

def speccheck(t, e):
  if isinstance(t, str):
    return predicates._get(t)(e)
  return t(e)



def dict_act(verb, *args):
  try:
    arity = len(args)
    cursor = walk(registry, verb)
    cursor = walk(cursor, arity)
    report = []
    rolereport = []
    if cursor:
      results = OD()   
      for role in cursor:      
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
  except Exception as exc:
    print exc, "\r\n", " ".join(report)
    raise



def call(verb, *args):
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







