from methods import *
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import components
from colors import *

def act(v,e,a):
  components.act(v,e,a)

def _symbol(s):
  try:
    return globals()[s]
  except:
    return False

def look_entity(e, n=False):
  m = wrap(name(e)+" looks at something", color("yellow"))
  send_room(e['located'], m)

def look_player(e, n=False):
  n = get_room(n)
  print "look_player(e, "+str(n)+")"
  e['player'].look(n)

def go_located(e, n):
  print "go_located"
  target = get_room(n)
  source = get_room(e['located'])
  if source and target:
    c = source['room']['contents']
    if e['uuid'] in c:
      c.remove(e['uuid'])
  if target:
    c = target['room']['contents']
    c.append(e['uuid'])
    e['located'] = target['id']
    act("arrive", e, target)

def arrive_player(e, room):
  print "arrive_player"
  act("look", e, room)
