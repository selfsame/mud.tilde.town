from mud.core import *


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

predicates.register("room", has("room", "exits"))
predicates.register("located", has("located"))

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
      chosen = parse.table_choice(choices)
      sp = components.instance(chosen)
      spawner['instances'].append(sp['uuid'])
      sp['located'] = r['id']
      components.register(sp)
      act("walk",sp,r)      
    spawner['timer'] = spawner['rate']
  else:
    spawner['timer'] = ap






