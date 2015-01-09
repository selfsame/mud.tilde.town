from mud.core import *

register("colored", has('color'))

def _color_is(c): 
  def hue(e):
    return e.get('color') == c
  return hue

register("yellow", _color_is("yellow"))
register("red", _color_is("red"))
register("green", _color_is("green"))

hidden = register("hidden", has("hidden"))

@after
@given(a("hidden", "thing"))
def indefinate_name(e):
  return "(hidden){#reset}"

@before
@given(a("hidden", "thing"))
def indefinate_name(e):
  return "{#bold}{#black}"


@before
@given(a("yellow", "thing"))
def printed_name(e):
  return "{#yellow}"

@before
@given(a("red", "thing"))
def printed_name(e):
  return "{#red}"

@after
@given(a("colored", "thing"))
def printed_name(e):
  return "{#reset}"
