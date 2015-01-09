from util import *
from mud.core import verbs

registry = {}

def register(s, f):
  registry[s] = f
  return s





def get(s):
  if s in registry: return registry[s]
  def key(e):
    if isinstance(e, dict):
      if s in e: return True
    return False
  return key



def anything(e):
  return True

def number(e):
  return isinstance(e, (int, float))

def integer(e):
  return isinstance(e, int)

def string(e):
  return isinstance(e, str)

def function(e):
  return str(type(e)) in ["<type 'function'>", "<type 'builtin_function_or_method'>"]

def dictionary(e):
  return isinstance(e, dict)

def module(e):
  return str(type(e)) == "<type 'module'>"

def undefined(e):
	if e == None: return True
	return False


def has(*args):
  def f(e):
    if isinstance(e, dict):
      for s in args:
        if isinstance(s, str):
          if s not in e: return False
        else: return False
      return True
    return False
  f.__name__ = "has("+"_".join(map(fn_name, args))+")"
  return f

def a(*args):
  def f(e):
    for spec in args:
      if isinstance(spec, str):
        p = get(spec)
        if not p(e): 
          return False
      elif function(spec):
        if not spec(e): return False
    return True
  f.__name__ = "_".join(map(fn_name, args))
  return f

def non(*args):
  def nf(x): 
    for f in args:
      if isinstance(f, str):
        p = get(f)
        if p(x): 
          return False
      elif f(x): return False
    return True
  nf.__name__ = "non("+"_".join(map(fn_name, args))+")"
  return nf

def equals(*a):
  def efn(b):
    for v in a:
      if b != v: return False
    return True
  return efn

def verb(e):
  if e in verbs.forms: return True
  return False
