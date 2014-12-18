from util import *

def number(e):
  return isinstance(e, (int, float))

def integer(e):
  return isinstance(e, int)

def single(e):
	def efn(b):
		return e == 1
	return efn

def string(e):
  return isinstance(e, str)

def dictionary(e):
  return isinstance(e, dict)

def undefined(e):
	if e == None: return True
	return False

def anything(e):
	return True

def equals(a):
	def efn(b):
		return a == b 
	return efn

def function(e):
  return str(type(e)) in ["<type 'function'>", "<type 'builtin_function_or_method'>"]

def odd(n):
  if number(n):
    if n % 2 == 1:
      return True
  return False

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

def isnt(posf):
  def negf(x):
    return not posf(x)
  return negf

def non(f):
  def nf(x): return not f(x)
  return nf

room = a('room')
thing = a('thing')
object = a('object')
entity = a('entity')
human = a('human')
player = a('player')
holder = a('contents')
container = a(holder, non(entity))
hidden = a('hidden')
located = a('located')



def closed(e):
  if e.get("closed") == True:
    return True
  return False

opened = non(closed)


def empty(e):
	if container(e):
		c = len(contents_of(e))
		if c == 0: return True
	return False


def idle(e):
	ap = the(the(e, "acting"), "ap")
	if ap == 0:
		return True
	return False




def male(subjects):
  if the(subjects, 'gender') == 'male': return True
  return False

def old(subjects):
  if the(subjects, 'age') > 70: return True
  return False

def young(subjects):
  if the(subjects, 'age') < 16: return True
  return False

female = a(non(male), 'human')
adult = a(non(old),non(young), 'human')
animal = a(non(human), 'entity')




colored = a('color')
def yellow(e): return e.get('color') == "yellow" 
def red(e): return e.get('color') == "red" 
def green(e): return e.get('color') == "green" 