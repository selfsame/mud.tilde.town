from util import *
from mud.core import verbs


def anything(e):
  return True

def number(e):
  return isinstance(e, (int, float))

def integer(e):
  return isinstance(e, int)

def string(e):
  return isinstance(e, str)

def dictionary(e):
  return isinstance(e, dict)

def module(e):
  return str(type(e)) == "<type 'module'>"

def undefined(e):
	if e == None: return True
	return False

def function(e):
  return str(type(e)) in ["<type 'function'>", "<type 'builtin_function_or_method'>"]

def thing(e):
  return dictionary(e)

def a(*args):
  def f(e):
    if not isinstance(e, dict):
      return False
    for spec in args:
      if string(spec):
        if spec not in e: return False
      elif function(spec):
        if not spec(e): return False
      else: return False
    return True
  f.__name__ = "_".join(map(fn_name, args))
  return f

def non(f):
  def nf(x): return not f(x)
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
