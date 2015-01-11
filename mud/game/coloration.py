from mud.core import *

bind.predicate("colored", has('color'))

def _color_is(c): 
  def hue(e):
    return e.get('color') == c
  return hue

bind.predicate("yellow", _color_is("yellow"))
bind.predicate("red", _color_is("red"))
bind.predicate("green", _color_is("green"))
bind.predicate("hidden", has("hidden"))

@after(a("hidden", "thing"))
def indefinate_name(e):
  return "(hidden){#reset}"

@before(a("hidden", "thing"))
def indefinate_name(e):
  return "{#bold}{#black}"


@before(a("yellow", "thing"))
def printed_name(e):
  return "{#yellow}"

@before(a("red", "thing"))
def printed_name(e):
  return "{#red}"

@after(a("colored", "thing"))
def printed_name(e):
  return "{#reset}"
