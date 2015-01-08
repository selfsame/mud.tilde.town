from mud.core.predicates import *
from mud.core.util import contents_of

room = a('room')
thing = a('thing')
object = a('object')
entity = a('entity')
human = a('human')
player = a('player')
hidden = a('hidden')

def located(e):
  if e.get('located'): return True
  return False

holder = a('contents')

container = a(holder, non(entity))

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