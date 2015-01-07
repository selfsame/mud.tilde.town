from mud.core.actions import *
from mud.core.util import *
from mud.core.predicates import *
import random


@after
@given(player, a(opened, container))
def look(p, r):
  say("Inside it you see "+ act("list_contents", p, r)+ ".")

@after
@given(player, a(empty, container))
def look(p, r):
  say("It's completely empty.")

@before
@given(a(closed, container))
def printed_name(e):
  return "closed "

@before
@given(a(opened, container))
def printed_name(e):
  return "open "

@after
@given(a(opened, container))
def indefinate_name(e):
  return " (containing "+act("list_contents", e)+")"

@after
@given(a(opened, empty, container))
def indefinate_name(e):
  return "(empty)"

@after
@given(a(hidden, thing))
def indefinate_name(e):
  return "(hidden){#reset}"

@before
@given(a(hidden, thing))
def indefinate_name(e):
  return "{#bold}{#black}"


@before
@given(a(yellow, thing))
def printed_name(e):
  return "{#yellow}"

@before
@given(a(red, thing))
def printed_name(e):
  return "{#red}"

@after
@given(a(colored, thing))
def printed_name(e):
  return "{#reset}"

@action
@given(entity, anything)
def open(a, b):
  say("You can't open that.")

@action
@given(entity, anything)
def close(a, b):
  say("You can't close that.")

@action
@given(entity, a(opened, container))
def open(a, b):
  say("It's allready opened.")

@action
@given(entity, a(closed, container))
def close(a, b):
  say("It's allready closed.")

@action
@given(entity, a(closed, container))
def open(a, b):
  b["closed"] = False
  relation = act("scope_relation", b, a)
  say("You open the "+name(b)+relation+".")
  report_to(location(a), act("indefinate_name", a), "opens the ", name(b)+relation+".")
  return True

@action
@given(entity, a(opened, container))
def close(a, b):
  b["closed"] = True
  relation = act("scope_relation", b, a)
  say("You close the "+name(b)+relation+".")
  report_to(location(a), act("indefinate_name", a), "closes the ", name(b)+relation+".")
  return True