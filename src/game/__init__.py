import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import parse
from components import load, instance, register, act
from components.methods import *
import data
from colors import *
from verbs import verbs
import re

class Game():
  def __init__(self):
    load('edit')
  def sendRoom(s):
    pass


class Player():
  def __init__(self, con, d):
    entity = instance("player")
    self.con = con
    self.data = dict(entity.items() + d.items())
    self.data['player'] = self
    register(self.data)
    print self.data
    if not self.data.get('located'):
      self.data['located'] = "lobby"
    act("go", self.data, self.data['located'])
    self.con.sendLine("\r\n\r\n\r\n")
    act("look", self.data, self.room())
  
  def room(self):
    return data.rooms.get(self.data['located'])

  def update(self, delta):
    pass

  def input(self, line):
    words = parse.words(line)
    self.con.sendLine("you entered words: "+str(words))
    scope = get_scope(self.data)
    res = []
    verb = False
    if len(words) > 0:
      for v in verbs:
        if re.match(v, words[0]):
          verb = verbs[v]
      if len(words) > 1:
        if verb:
          target = resolve_noun(words[1], scope)
          act(verb, self.data, target)
      elif verb:
        act(verb, self.data, resolve_noun("", scope))

  def look(self, thing):
    print self.room()
    res = ["\r\n",
           wrap(name(thing), color('green')),
           description(thing),
           "",
           "exits: "+", ".join(has(thing, "exits", {"none":0}).keys())]
    self.con.sendLine("\r\n".join(res))

def get_scope(entity):
  "returns a list of entity instances in scope of the actor"
  res = [entity]
  location = has(entity, 'located')
  room = data.rooms.get(location)
  if room:
    res.append(room)
  print "SCOPE"
  for e in res:
    print e['id']
  return res

def resolve_noun(s, scope):
  "given a word and a list of entities in scope, determine what is meant"
  rooms = []
  entities = []
  objects = []
  for e in scope:
    if s == e['id']:
      return e['id']
    if has(e, 'room'):
      rooms.append(e)
  for r in rooms:
    for k in r['exits']:
      if s == k:
        return r['exits'][k]
  return rooms[0]['id']
