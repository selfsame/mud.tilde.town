    #!/usr/bin/env python

from twisted.internet import reactor, task
from twisted.internet.protocol import ServerFactory 
from twisted.protocols.basic import LineOnlyReceiver

import time
import player
import functions
from login import login
from intro import intro
from create import create

class MUDProtocol(LineOnlyReceiver):
    ## Connection object, will be hooked up to player object
    def __init__(self):
        self.status = 0 #used for login state machine
        self.safename = "guest"
        self.password = "guest"
        self.new = 0
        self.dopple = 0
        

    def lineReceived(self, line):
        if self.status < 3: #checking name / password
            login(self, line)
        elif self.status == 3: #creating a character
            if create(self.player, line, self.new): #if create dialogue finished
                self.status = 4
        elif self.status == 4: 

            
            self.factory.playerObjects.append(self.player)
            self.factory.broadOthers(self, "\033[01;35m" + self.player.name+ " has logged in." + "\033[01;37m")
            self.sendLine("\033[01;35m" + "Welcome to the world, "+ self.player.name + "\033[01;37m")
            self.status = 5
            self.player.updateRoom()
            print "ClientProtocols: ", len( self.factory.clientProtocols )
                
        elif self.status == 5: #now in game    
            self.player.handle(line)
        
    def sendLine(self, line): 
        self.transport.write(line+"\r\n")
    
    def connectionMade(self):
        print self.factory
        intro(self)
        self.factory.clientProtocols.append(self)

class ChatProtocolFactory(ServerFactory): 

    protocol = MUDProtocol 

    def __init__(self): 
        self.clientProtocols = []
        self.playerObjects = []
        self.islands = functions.parseIslands(".\\edit\\islands\\", self)
        self.monsters = functions.parseMonsters("./edit/entities/")
        self.items = functions.parseItems(".\\edit\\items\\")
        
        loopingCall = task.LoopingCall(self.timeDisbatch)
        loopingCall.start(.5)

    def broadcast(self, mesg): #This should go to any state client
        
        for client in self.clientProtocols:
            client.sendLine(mesg)
            
    def broadOthers(self, me, mesg):   #This should send to all playerobjects, so no spam to login   
        for client in self.playerObjects:
            if client != me:
                client.sendLine(mesg)

    def timeDisbatch(self):
        for entry in self.playerObjects:
                entry.update(time.time())
        for entry in self.islands:
            for item in self.islands[ entry ].roomlist:
                self.islands[ entry ].roomlist[ item ].update(time.time())

def Main():
    
    print "Starting IslandsMUD DEVELOPMENTAL server"
    factory = ChatProtocolFactory()
    reactor.listenTCP(5071, factory)

    
    
    reactor.run()
    
    


if __name__== '__main__' :Main()
