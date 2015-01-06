import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from actions import *
from util import *
from predicates import *
import random


@action
@given(a("acting"), number)
def update(a, delta):
  ap = a['acting']['ap']
  ap -= delta
  if ap < 0: ap = 0
  a['acting']['ap'] = ap

@action
@given(a("wandering", idle, entity), number)
def update(a, delta):
  loc = location(a)
  if room(loc):
    dests = connected_rooms(loc)
    dest = random.choice(dests)
    if act("walk", a, dest):
      a['acting']['ap'] = 30 + random.randint(1, 20)




@action
@given(entity, room)
def walk(a, b):
  loc = location(a)
  if act("move", a, b):
    if loc:
      exits = the(loc,"exits")
      exit = False
      for k in exits:
        if exits[k] == the(b, "id"):
          exit = k 
      act("leave", loc, a, exit)
    act("arrive", a, b)
    return True
  return False

@action
@given(room, entity, string)
def leave(o, e, b):
  report_to(o, "{#black}{#bold}"+act("indefinate_name", e), "leaves to the", b+".{#reset}")

@action
@given(entity, room)
def arrive(e, r):
  report_to(r,  "{#black}{#bold}"+act("indefinate_name", e), "walks in.{#reset}")


@action
@given(thing)
def printed_name(a):
  return name(a)




@action
@given(a('uuid', thing), holder)
def move(a, b):
  uid = the(a, 'uuid')
  dest = the(b, 'contents')
  try:
    dest.append(uid)
    return True
  except:
    print "fail move:", uid, dest
    return False

@action
@given(a('located', 'uuid', thing), holder)
def move(a, b):
  uid = the(a, 'uuid')
  loc = location(a)
  source = the(loc, 'contents')
  dest = the(b, 'contents')
  try:
    if uid in source: source.remove(uid)
    dest.append(uid)
    a['located'] = ""
    return True
  except:
    print "fail move:", uid, loc, source, dest
    return False

@after
@given(a('uuid', thing), holder)
def move(a, b):
  a['located'] = b['uuid']

@after
@given(a('uuid', thing), room)
def move(a, b):
  a['located'] = b['id']





@before
@given(a(located, thing))
def delete(e):
  print "deleting uid from holding room"
  loc = location(e)
  if room(loc):
    uuid = e.get("uuid")
    if uuid in loc['contents']:
      loc['contents'].remove(uuid)

@action
@given(thing)
def delete(e):
  print "deleting ",name(e) ,"container contents"
  components.delete(e)

@action
@given(holder)
def delete(e):
  print "deleting ",name(e) ,"container contents"
  map(components.delete, contents_of(e))
  components.delete(e)


