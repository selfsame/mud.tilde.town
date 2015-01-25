from mud.core.util import *
from mud.core import *

@given()
def init():
  print "\n\n(init)"
  data.game["rooms"] = {}
  for k in data.datatypes:
    e = data.datatypes[k]
    if e.get("room"):
        if not e.get("base"):
            data.instance(e.get("id"))

  

@given("room")
def register(r):
  print 'register: ', util.name(r)
  data.game["rooms"][r["id"]] = r

@after()
def init():
  print "\n==rooms==============================================="
  print data.game["rooms"].keys()
  print "==datatypes============================================"
  print data.datatypes.keys()




@given("holder")
def init(r):
  print "init(holder)", name(r)
  cont = call("get_contents", r)
  if isinstance(cont, list):
    for e in cont:
      e["located"] = r.get("uuid")

@given("room")
def init(r):
  print "init(holder)", name(r)
  cont = call("get_contents", r)
  if isinstance(cont, list):
    for e in cont:
      e["located"] = r.get("id")


@given(number)
def update(delta):
  for id in data.game["rooms"]:
    call("update", data.game["rooms"][id], delta)


@given("holder", number)
def update(r, delta):
  contents = r['contents']
  for uid in contents:
    if uid in data.instances:
        stack("update", data.instances[uid], delta)