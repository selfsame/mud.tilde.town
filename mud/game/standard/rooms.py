from mud.core.util import *
from mud.core.actions import *
from mud.core.predicates import *
import random
from mud.core.parse import table_choice
from mud.core.components import *
from mud.core import data



@action
@given(a("spawning", room), number)
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
      print "SPAWN:", chosen
      sp = instance(chosen)
      spawner['instances'].append(sp['uuid'])
      sp['located'] = r['id']
      register(sp)
      act("walk",sp,r)      
    spawner['timer'] = spawner['rate']
  else:
    spawner['timer'] = ap