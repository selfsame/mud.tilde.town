from mud.core.util import *
from mud.core import *

@given()
def init():
  print "\n\n(init)"
  for k in data.datatypes:
    e = data.datatypes[k]
    if e.get("room"):
        if not e.get("base"):
            data.instance(e.get("id"))
  for k in data.rooms:
      call("init", data.rooms[k])

@after()
def init():
  print "\n==rooms==============================================="
  print data.rooms.keys()
  print "==datatypes============================================"
  print data.datatypes.keys()


@given("holder")
def init(r):
  cont = contents_of(r)
  for e in cont:
    e["located"] = r.get("uuid")
    call("init", e)

@given(number)
def update(delta):
  for room in data.rooms:
    call("update", data.rooms[room], delta)


@after("room", number)
def update(r, delta):
  contents = r['contents']
  data.scope = map(from_uid, contents)    
  for uid in contents:
    if uid in data.instances:
        call("update", data.instances[uid], delta)