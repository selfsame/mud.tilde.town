from mud.core.util import *
from mud.core import *
import random


bind.predicate("entity", has("entity"))

def idle(e):
  if dictionary(e):
    if e.get("ap") == 0:
      return True
  return False

bind.predicate("idle", has("idle"))


@construct
def living(d):
    hpmax = d['hpmax']
    if parse.dice.is_dice(d['hpmax']):
        hpmax = parse.dice.roll(d['hpmax'])
    d['hp'] = hpmax
    d['hpmax'] = hpmax
    return d

@construct
def inventory(d):
  return {"contents":[]}

@construct
def acting(d):
  d["ap"] = random.randint(20,50)
  return d




@given(has("acting"), number)
def update(a, delta):
  ap = a['acting']['ap']
  ap -= delta
  if ap < 0: ap = 0
  a['acting']['ap'] = ap

@given(a("wandering", "idle", "entity"), number)
def update(a, delta):
  loc = location(a)
  if has("room")(loc):
    dests = connected_rooms(loc)
    dest = random.choice(dests)
    if call("walk", a, dest):
      a['acting']['ap'] = 30 + random.randint(1, 20)


@given("entity", "room")
def walk(a, b):
  loc = location(a)
  if call("move", a, b):
    if loc:
      exits = the(loc,"exits")
      exit = False
      for k in exits:
        if exits[k] == the(b, "id"):
          exit = k 
      call("leave", loc, a, exit)
    call("arrive", a, b)
    return True
  return False

@given("room", "entity", string)
def leave(o, e, b):
  report_to(o, "{#bold}"+call("indefinate_name", e), "leaves to the", b+".{#reset}")

@given("entity", "room")
def arrive(e, r):
  report_to(r,  "{#bold}"+call("indefinate_name", e), "walks in.{#reset}")



