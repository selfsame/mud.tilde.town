import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import parse
import components
from components import load, instance, register
from actions import *
from util import *
import data
import random
from player import Player

class Game():
  def __init__(self):
    load(os.sep.join(['./edit']))
    print "\n==rooms==============================================="
    print data.rooms.keys()
    print "==datatypes============================================"
    print data.datatypes.keys()
    print "--entities----------------------------------------------"
    print data.entities.keys()
    print "--objects----------------------------------------------"
    print data.objects.keys()
    print "\n\n"
    self.place("lobby", "mouse")
    self.place("r1", "key")
    self.place("lobby", "book")
    for k in data.rooms:
        act("init", data.rooms[k])

  def update(self,delta):
    data.subject = {}
    for room in data.rooms:
      contents = data.rooms[room]['contents']
      data.scope = map(from_uid, contents)    
      for uid in contents:
        if uid in data.instances:
            act("update", data.instances[uid], delta)



  def place(self, roomid, thingid):
    room = data.rooms.get(roomid)
    thing = data.datatypes.get(thingid)
    inst = instance(thingid)
    register(inst)
    room['contents'].append(inst['uuid'])
    inst['located'] = room['id']
    return inst

  def sendRoom(s):
    pass





# data.game.place("lobby", "mouse")
# data.game.place("r1", "key")
# data.game.place("lobby", "book")


# player = Player([], {"name":"Joe"})



# player.input("get book")


# data.game.update(12)
# player.input("look")

# player.input("go east")
# player.input("look")

# player.input("go door")
# player.input("look")






