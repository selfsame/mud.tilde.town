from mud.core import *
from CAPSMODE import *

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

bind.predicate("room", has("room", "exits"))
bind.predicate("located", has("located"))

@given("room")
def connections(r):
  es = r["exits"]
  res = []
  for s in es:
    er = data.game["rooms"].get(es[s])
    if er: res.append(er)
  return res

@given("located")
def get_location(e):
  r = GET(data.game["rooms"], e["located"])
  if r: return r
  r = GET(data.instances, e["located"])
  if r: return r
  print "NO LOCATION FOR", util.name(e)


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
      chosen = parse.table_choice(choices)
      sp = data.instance(chosen)
      spawner['instances'].append(sp['uuid'])
      sp['located'] = r['id']
      call("walk",sp,r)      
    spawner['timer'] = spawner['rate']
  else:
    spawner['timer'] = ap






