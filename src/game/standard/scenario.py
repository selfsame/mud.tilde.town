import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from required import *
from actions import *
import data
from util import *
from predicates import *
import random
from components import load, instance, register

@action
@given()
def init():
  print "\n\n(init)"
  for k in data.datatypes:
    e = data.datatypes[k]
    if e.get("room"):
        if not e.get("base"):
            register(instance(e.get("id")))    
  for k in data.rooms:
      act("init", data.rooms[k])

@after
@given()
def init():
  print "\n==rooms==============================================="
  print data.rooms.keys()
  print "==datatypes============================================"
  print data.datatypes.keys()

@action
@given(holder)
def init(r):
  print "    room:", name(r)
  cont = contents_of(r)
  for e in cont:
    e["located"] = r.get("uuid")
    act("init", e)

@action
@given(number)
def update(delta):
  for room in data.rooms:
    act("update", data.rooms[room], delta)


@after
@given(room, number)
def update(r, delta):
  contents = r['contents']
  data.scope = map(from_uid, contents)    
  for uid in contents:
    if uid in data.instances:
        act("update", data.instances[uid], delta)