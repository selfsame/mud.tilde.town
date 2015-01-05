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
    for k in data.datatypes:
        e = data.datatypes[k]
        if e.get("room"):
            if not e.get("base"):
                register(instance(e.get("id")))    
    for k in data.rooms:
        act("init", data.rooms[k])
    self.report_data()

  def update(self,delta):
    data.subject = {}
    for room in data.rooms:
      act("update", data.rooms[room], delta)
      contents = data.rooms[room]['contents']
      data.scope = map(from_uid, contents)    
      for uid in contents:
        if uid in data.instances:
            act("update", data.instances[uid], delta)
        else:
            print "\rn\rnUNREGISTERED  ",uid,"\rn\rn"



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

  def report_data(self):
    print "\n==rooms==============================================="
    print data.rooms.keys()
    print "==datatypes============================================"
    print data.datatypes.keys()
    print "--entities----------------------------------------------"
    print data.entities.keys()
    print "--objects----------------------------------------------"
    print data.objects.keys()
    print "\n\n"










