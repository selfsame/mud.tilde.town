import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from core import *
from util import *
from predicates import *
import random

@action
@given(number)
def written(n):
  table = {1:"one",2:"two",3:"three",4:"four",5:"five",6:"six",
          7:"seven",8:"eight",9:"nine",10:"ten",11:"eleven",12:"twelve"}
  res = table.get(n)
  return res or "many"

@action
@given(thing, string)
def write(e,p):
  if e.get(p):
    return e.get(p)
  else:
    return "<no "+p+">"

@action
@given(thing)
def indefinate_article(a):
  return act("indefinate_article", name(a))


@action
@given(string)
def indefinate_article(a):
  if a[0] in ["a", "o", "i", "e"]:
    return "an "
  else:
    return "a "

@action
@given(number, string)
def indefinate_article(n, a):
  if n >= 2:
    return act("written", n)+" "
  return act("indefinate_article", a)

@action
@given(thing)
def plural_name(a):
  p = the(a, "plural")
  if p: return p
  return act("printed_name", a) + "s"


@action
@given(number, thing)
def definate_article(n, a):
  return "the "

@action
@given(thing)
def definate_article(n, a):
  return "the "

@action
@given(anything, anything)
def indefinate_name(n, e):
  return "a thing"



@action
@given(number, thing)
def indefinate_name(n, e):
  noun = "".join(act_stack("plural_name", e))
  return str(act("indefinate_article", n, noun))+ noun


@action
@given(thing)
def indefinate_name(e):
  noun = "".join(act_stack("printed_name", e))
  return str(act("indefinate_article", noun))+ noun

@action
@given(player)
def indefinate_name(e):
  noun = "".join(act_stack("printed_name", e))
  return noun.title()




