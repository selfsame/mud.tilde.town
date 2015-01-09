from mud.core.util import *
from mud.core.actions import *
from predicates import *
import random
from mud.core.parse import table_choice
from mud.core.components import *
from mud.core import data, predicates, parse

def located(e):
  if dictionary(e):
    if e.get("located"): return True
  return False

predicates.register("room", has("room", "exits"))
predicates.register("located", located)

@action
@given("room")
def connections(r):
  es = r["exits"]
  res = []
  for s in es:
    er = data.rooms.get(es[s])
    if er: res.append(er)
  return res

@action
@given(a("spawning", "room"), number)
def update(r, delta):
  spawner = r['spawning']
  ap = spawner['timer']
  ap -= delta
  if ap < 0:
    dead = []
    for uid in spawner['instances']:
      if uid not in data.instances:
        dead.append(uid)
    for d in dead:
      spawner['instances'].remove(d)
    count = len(spawner['instances'])
    if count < spawner['max']:
      choices = spawner['choices']
      chosen = table_choice(choices)
      sp = instance(chosen)
      spawner['instances'].append(sp['uuid'])
      sp['located'] = r['id']
      register(sp)
      act("walk",sp,r)      
    spawner['timer'] = spawner['rate']
  else:
    spawner['timer'] = ap


@construct
def exits(d):
  res = {}
  for ustr in d:
    dtype = data.datatypes.get(d[ustr])
    if dtype:
      res[ustr] = d[ustr]
  return d

@construct
def spawning(d):
  res = {"rate":100, "max":5, "instances":[]}
  res = dict(res.items() + d.items())
  res["timer"] = 0
  return res

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

