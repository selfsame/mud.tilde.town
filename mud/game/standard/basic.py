from mud.core import *
from mud.core.util import *

@given("thing")
def printed_name(a):
  return name(a)

def _located(e):
  if has("located")(e):
    if GET(data.instances, GET(e, "located")): return True
    if GET(data.game["rooms"], GET(e, "located")): return True
  return False

bind.predicate("located", _located)

@given("registered", "holder")
def move(a, b):
  uid = a['uuid']
  dest = b['contents']
  try:
    dest.append(uid)
    return True
  except:
    print "fail move:", uid, dest
    return False

@given("located", "holder")
def move(a, b):
  uid = a['uuid']
  loc = location(a)
  source = GET(loc,"contents")
  dest = GET(b,"contents")
  try:
    if uid in source:
      source.remove(uid)
    dest.append(uid)
    return True
  except:
    print "fail move:", uid, map(util.name, [a, b]), source
    return False

@after("thing", "holder")
def move(a, b):
  a['located'] = b['uuid']

@after("thing", "room")
def move(a, b):
  a['located'] = b['id']

@before(a("located", "thing"))
def delete(e):
  print "deleting uid from holding room"
  loc = call("get_location", e)
  if bound("room")(loc):
    uuid = e.get("uuid")
    if uuid in loc['contents']:
      loc['contents'].remove(uuid)

@given("thing")
def delete(e):
  print "deleting ",name(e) ,"container contents"
  data.delete(e)

@given("holder")
def delete(e):
  print "deleting ",name(e) ,"container contents"
  map(data.delete, call("get_contents", e))
  data.delete(e)


