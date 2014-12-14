import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from core import *
from util import *
from predicates import *
import random


@after
@given(player, container)
def look(p, r):
  say("Inside it you see "+ act("list_contents", p, r)+ ".")

@after
@given(player, a(empty, container))
def look(p, r):
  say("It's completely empty.")

@before
@given(a(non(open), a(non(entity), container)))
def printed_name(e):
  return "closed "

@before
@given(a(open, container))
def printed_name(e):
  return "open "

@after
@given(a(open, container))
def indefinate_name(e):
  return "({#black}containing "+act("list_contents", e)+"{#reset})"

@after
@given(a(open, empty, container, non(entity)))
def indefinate_name(e):
  return "(empty)"

@after
@given(a(hidden, thing))
def indefinate_name(e):
  return "(hidden){#reset}"

@before
@given(a(hidden, thing))
def indefinate_name(e):
  return "{#black}"


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