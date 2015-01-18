from mud.core import *
import random

bind.predicate("colored", has('color'))

@construct
def color(c):
	if c == "random":
		return random.choice(["yellow","brown","red","green","cyan","magenta"])
	return c

def _color_is(c): 
  def hue(e):
    return e.get('color') == c
  return hue

bind.predicate("yellow", _color_is("yellow"))
bind.predicate("brown", _color_is("brown"))
bind.predicate("red", _color_is("red"))
bind.predicate("green", _color_is("green"))
bind.predicate("cyan", _color_is("cyan"))
bind.predicate("magenta", _color_is("magenta"))
bind.predicate("hidden", has("hidden"))

bind.adjective("colored", "colored")
bind.adjective("red", "red")
bind.adjective("yellow", "yellow")
bind.adjective("brown", "brown")
bind.adjective("green", "green")
bind.adjective("cyan", "cyan")
bind.adjective("magenta", "magenta")

@after(a("hidden", "thing"))
def indefinate_name(e):
  return "(hidden){#reset}"

@before(a("hidden", "thing"))
def indefinate_name(e):
  return "{#bold}{#black}"


@before(a("cyan", "thing"))
def printed_name(e):
  return "{#bold}{#cyan}"

@before(a("magenta", "thing"))
def printed_name(e):
  return "{#bold}{#magenta}"

@before(a("yellow", "thing"))
def printed_name(e):
  return "{#bold}{#yellow}"

@before(a("green", "thing"))
def printed_name(e):
  return "{#green}"

@before(a("brown", "thing"))
def printed_name(e):
  return "{#yellow}"

@before(a("red", "thing"))
def printed_name(e):
  return "{#red}"

@after(a("colored", "thing"))
def printed_name(e):
  return "{#reset}"
