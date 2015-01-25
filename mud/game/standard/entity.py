from mud.core.util import *
from mud.core import *
import random
from mud.core.CAPSMODE import *
import copy

bind.predicate("entity", has("entity"))

def idle(e):
  if GET(e,"acting"):
    if GET(e["acting"],"ap", 100) <= 0:
      return True
  return False

bind.predicate("idle", idle)


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
  return copy.copy(d)






@given(has("acting"), number)
def update(a, delta):
  ap = a['acting']['ap']
  ap -= delta * 10
  if ap < 0: ap = 0
  a['acting']['ap'] = ap

@before(has("living"), number)
def update(a, delta):
  hp = a["living"]["hp"]
  hpmax = a["living"]["hpmax"]
  hp += 0.1
  if hp > hpmax: hp = hpmax
  a["living"]["hp"] = hp

@given(a(has("wandering"), "idle", "entity"), number)
def update(a, delta):
  a['acting']['ap'] = 10 + random.randint(10, 30)
  if random.randint(0, 20) < 2:
    loc = location(a)
    if has("room")(loc):
      dests = connected_rooms(loc)
      dest = random.choice(dests)
      call("enact", a, "walk", dest)


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
    understood.scope(call("get_contents", b))
    call("arrive", a, b)
    understood.previous()
    return True
  return False

@given("player", string)
def walk(a, b):
  loc = location(a)
  exits = the(loc, "exits")
  for k in exits:
    if b == k:
      v = exits[k]
      r = data.game["rooms"].get(v)
      if call("move", a, r):
        call("leave", loc, a, k)
        understood.scope(call("get_contents", r))
        call("arrive", a, r)
        understood.previous()


@given("room", "entity", string)
def leave(o, e, b):
  report("[Subject] leave[s] to the "+b+".")


@given("entity", "room")
def arrive(e, r):
  understood.subject(e)
  sc = copy.copy(understood.scope())
  if e in sc:
    sc.remove(e)
  understood.scope(sc)
  report("[Subject] walk[s] in.")
  understood.previous().previous()



