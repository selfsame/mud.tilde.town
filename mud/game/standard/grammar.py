from mud.core.util import *
from mud.core import *


@given(number)
def written(n):
  table = {1:"one",2:"two",3:"three",4:"four",5:"five",6:"six",
          7:"seven",8:"eight",9:"nine",10:"ten",11:"eleven",12:"twelve"}
  res = table.get(n)
  return res or "many"

@given("thing", string)
def write(e,p):
  if e.get(p):
    return e.get(p)
  else:
    return "<no "+p+">"

@given("thing")
def indefinate_article(a):
  return call("indefinate_article", name(a))


@given(string)
def indefinate_article(a):
  if a[0] in ["a", "o", "i", "e"]:
    return "an "
  else:
    return "a "

@given(number, string)
def indefinate_article(n, a):
  if n >= 2:
    return call("written", n)+" "
  return call("indefinate_article", a)

@given("thing")
def plural_name(a):
  p = the(a, "plural")
  if p: return p
  return call("printed_name", a) + "s"


@given(number, "thing")
def definate_article(n, a):
  return "the "

@given("thing")
def definate_article(n, a):
  return "the "

@given(anything, anything)
def indefinate_name(n, e):
  return "a thing"



@given(number, "thing")
def indefinate_name(n, e):
  noun = "".join(act_stack("plural_name", e))
  return str(call("indefinate_article", n, noun))+ noun


@given("thing")
def indefinate_name(e):
  noun = "".join(act_stack("printed_name", e))
  return str(call("indefinate_article", noun))+ noun

@given("player")
def indefinate_name(e):
  noun = call("printed_name", e)
  return noun




