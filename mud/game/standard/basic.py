from mud.core.actions import *
from mud.core.predicates import *
from mud.core import components



@action
@given("thing")
def printed_name(a):
  return name(a)

@action
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

@action
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

@after
@given("thing", "holder")
def move(a, b):
  a['located'] = b['uuid']

@after
@given("thing", "room")
def move(a, b):
  a['located'] = b['id']





@before
@given(a("located", "thing"))
def delete(e):
  print "deleting uid from holding room"
  loc = location(e)
  if get("room")(loc):
    uuid = e.get("uuid")
    if uuid in loc['contents']:
      loc['contents'].remove(uuid)

@action
@given("thing")
def delete(e):
  print "deleting ",name(e) ,"container contents"
  components.delete(e)

@action
@given("holder")
def delete(e):
  print "deleting ",name(e) ,"container contents"
  map(components.delete, contents_of(e))
  components.delete(e)


