from mud.core import *
from mud.core.util import *

@given("thing")
def printed_name(a):
  return name(a)

@given(a("registered", "thing"), "holder")
def move(a, b):
  uid = a['uuid']
  dest = b['contents']
  try:
    dest.append(uid)
    return True
  except:
    print "fail move:", uid, dest
    return False

@given(a("located", "registered", "thing"), "holder")
def move(a, b):
  uid = a['uuid']
  loc = location(a)
  source = loc['contents']
  dest = b['contents']
  try:
    if uid in source: source.remove(uid)
    dest.append(uid)
    return True
  except:
    print "fail move:", uid, loc, source, dest
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
  loc = location(e)
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
  map(data.delete, contents_of(e))
  data.delete(e)


