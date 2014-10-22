from random import randint, choice
import copy
from combat import *

class island:
    def __init__(self):
        self.name = "void"
        self.id = 0
        self.desc = []
        self.roomlist = {}
        

class room:
    def __init__(self, factory):
        self.factory = factory
        self.name = "void"
        self.id = 0
        self.desc = []
        self.exits = []
        self.monsters = container()
        self.players = container()
        self.items = container()
        self.spawn = []
        self.time = -1 #init
        self.timeidle = 0

    def hasplayers(self):
        if self.players != []:
            return 1

    def sendinroom(self, message):
        for entry in self.players:
            entry.sendLine( message )
    
    def update(self, time):
        
        if self.hasplayers():
            for entry in self.spawn:
                
                if randint(1,100) == 1:
                    x = 0
                    for i in range(entry[1][0]):
                        if randint(1, entry[1][1]) == 1:
                            x = 1
                            break
                    if x == 1:
                        newmonster = copy.deepcopy( self.factory.monsters[entry[0]] )
                        self.monsters.append( newmonster )
                        newmonster.init(self, self.factory)
                        self.sendinroom( "A "+newmonster.name + " has arrived." )
            for entry in self.monsters:
                entry.update(time)

class item:
    def __init__(self):
        self.id = 0
        self.name = "void"
        self.desc = []
        self.value = 0

class container(list):
    def __init__(self):
        super(container, self).__init__()
        self.room = 0
        self.player = 0

    def listcontents(self, exclude=0):
        stuff = {}
        for entry in self:
            if stuff.has_key(entry.name):
                stuff[entry.name] += 1
            elif entry != exclude:
                stuff[entry.name] = 1
        things = ""
        for entry in stuff:
            g = ""
            if stuff[entry] > 1:
                g = str(stuff[entry])+" "+entry+"s, "
            else:
                g = entry+", "
            things += g
        things = things[:-2]+"."
        
        return things
    
    def get(self, what):
        #use a name to pop first object with name match
        i = 0
        for entry in self:
            g = len( what )
            if what in entry.name[:g]:
                return self.pop(i)
                break
            i += 1

    def getself(self, what):
        #use object comparison to pop object
        i = 0
        for entry in self:
            if what == entry:
                return self.pop(i)
                break
            i += 1

    def count(self, what):
        i = 0
        for entry in self:
            l = len( what )
            if what in entry.name[:l]:
                i += 1
        return i
        


class monster:
    def __init__(self):
        self.factory = 0
        self.id = 0
        self.name = "void"
        self.desc = []
        self.hp = 0
        self.attacks = []
        self.drops = []
        self.room = 0
        self.cooldown = 0
        self.time = 0
        self.target = 0
        self.level = 0
        

    def update(self, time):
        self.time = time
        self.attack()

    def init(self, room, factory):
        self.room = room
        self.factory = factory
        self.exp = self.hp

    def die(self):
        for entry in self.drops:
            if randint(1, entry[1][1]) == 1:
                self.room.items.append( copy.deepcopy( self.factory.items[entry[0]] ) )
        try:
            self.room.monsters.getself( self )
        except:
            print "error removing dead monster"
        self.room.sendinroom( "The "+self.name+" dies." )
        del self
        

    def hurt(self, who, howmuch):
        self.target = who
        self.hp -= howmuch
        if self.hp <= 0:
            who.exp += self.exp
            who.target = 0
            self.die()
            
    
    def attack(self):
        
        if abs( self.cooldown - self.time ) > 3:
            if self.target in self.room.monsters or self.target in self.room.players:
                self.cooldown = self.time
                attack(self, self.target, self.room)
                


