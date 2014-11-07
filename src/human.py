from objects import *
from colors import *
from combat import *
from functions import pMatch

class human(object):
    def __init__(self, time, factory):
        super(human, self).__init__()

        self.factory = factory
        self.islands = factory.islands

        self.name = ""
        
        self.time = time
        
        self.sex = "m"
        self.stats = { "strength":8, "vitality":8, "agility":8, "intuition":8, "knowledge":8, "perception":8, "attractiveness":8 }

        self.skills = { "melee":0, "dancing":0, "mercantile":0, "navigation":0, "mapmaking":0, "seamanship":0, "carpentry":0, "smithing":0,
                        "engineering":0, "firearms":0, "munitions":0, "sailing":0, "stealth":0, "doctoring":0, "letter writing":0 }


        
        
        self.hpmax = 12
        self.hp = self.hpmax
        self.level = 1
        self.attacks = [["hit",[1,4]]] # temp base damage
        self.exp = 0
        
        self.deaths = 0
        self.kills = 0

        self.items = container()
        
        self.cooldown = self.time
        self.healtime = self.time

        self.islandName = "skullcap"
        self.roomName = "touroffice"

        self.island = 0
        self.room = 0

    ## First lets catch any functions intended for players
    ## Later on these can be used to trigger logic in the NPC class
    def sendLine(self, what):
        pass
    def sendPrompt(self, prompt):
        pass
    def quit(self):
        pass
    def status(self):
        pass
    

    def others(self, message): #message players in room
        olist = []
        for entry in self.room.players:
            if entry != self:
                    olist.append( entry )
        for entry in olist:
            entry.sendLine( message )    

    def updateRoom(self):
        
        self.island = self.islands[ self.islandName ]
        self.room = self.island.roomlist[ self.roomName ]
        if self not in self.room.players:
            self.room.players.append(self)

    def go(self, args=[]):
        where = args[1:]
        success = 0
        if where == []:
            self.sendLine( "Go where?" )
        else:
            for entry in self.room.exits:
                for word in entry[1].lower().split(" "):
                    if pMatch( where[0], word ): 
                        
                        self.others( self.name + " goes to the " + entry[1] + "." )
                        
                        self.room.players.getself(self)
                        failroom = self.room
                        self.roomName = entry[0]
                        self.others( self.name + " walks in from the " + entry[1] + "." )
                        try:
                            self.updateRoom()
                        except:
                            self.sendLine( "error, some location not made" )
                            self.roomName = failroom
                        self.look()
                        success = 1
                        break
                if success == 1:
                    break
            
            if success == 0:
                self.sendLine( "You can't go there." )




    
