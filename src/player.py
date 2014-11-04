
from colors import *
from combat import *
from functions import formatinput, pMatch
from objects import *
import pickle
from random import randint, choice
from human import *

class player(human):
    def __init__(self, protocol, factory, time):
        super(player, self).__init__(time, factory)
        #these must be unpacked before saving
        self.protocol = protocol
        
        
        self.idletime = time
        
        self.target = 0

        #persistant
        
        self.logged = 0
        self.password = ""

        
        self.desc = ["This is another player."]

##############################################
#           Internal Functions               #
##############################################

    def save(self): #need to clear internal pointers to higher objects before pickle dump of player, then restore
        tmpP = self.protocol
        tmpF = self.factory
        tmpT = self.time
        tmpI = self.idletime
        tmpS = self.islands
        
        
        self.protocol = 0
        self.factory = 0
        self.time = 0
        self.idletime = 0
        self.islands = 0
        self.island = 0
        self.room = 0
        
        self.target = 0 #just cleared
        
        savefile = open('./players/'+self.name+'.sav', 'w')
        pickle.dump(self, savefile)
        savefile.close()
        
        self.protocol = tmpP
        self.factory = tmpF
        self.time = tmpT
        self.idletime = tmpI
        self.islands = tmpS
        self.updateRoom()
        
    def sendLine(self, line):
        self.protocol.transport.write(line+"\r\n")

    def sendPrompt(self, prompt):
        self.protocol.transport.write(prompt)


    def status(self):
        self.sendPrompt( "HP:"+str(self.hp)+"/"+str(self.hpmax)+" >" )


    

    def update(self, time): #Player
        self.time = time
        timeidle = time - self.idletime
        self.heal()
        if abs(timeidle) > 300:
            self.sendLine("Idle too long, logging you out.")
            self.quit()
        if self.target != 0:
            self.attack()

    def heal(self): #Human
        if abs( self.healtime - self.time ) > 20:
            self.levelcheck()
            self.hp += int( self.hpmax/10 + randint(1, 2) )
            if self.hp > self.hpmax:
                self.hp = self.hpmax
            self.healtime = self.time

    def die(self): #Player
        self.room.sendinroom( background("red")+self.name+" has died!" + background("black"))
        try:
            self.room.players.remove( self ) # ?
        except:
            print "error removing dead player"
        self.roomName = "altar" 
        self.islandName = "skullcap"
        self.target = 0
        self.hp = self.hpmax
        penalty = int(self.exp*.1)
        self.exp -= penalty
        self.factory.broadOthers(self, color("yellow")+self.name+" has died."+color('white') )
        self.sendLine( str(penalty)+" exp penalty.")
        self.save()

    def attack(self):
        if abs( self.cooldown - self.time ) > 3:
            if self.target in self.room.monsters or self.target in self.room.players:
                self.cooldown = self.time
                attack(self, self.target, self.room)
                if self.target != 0:
                    if self.target.hp <= 0 or self.target.room == 5:
                        self.target = 0

    def hurt(self, who, howmuch):
        self.hp -= howmuch
        if self.hp <= 0:
            who.target = 0
            try:
                if who.logged > 0:
                    who.kills += 1
                    self.deaths += 1
            except:
                pass
            self.die()

    def levelcheck(self):
        if self.exp > int( (self.level*2 ** self.level)*.1 + self.level*70):
            self.level += 1
            self.hpmax += randint(1,3)+7
            self.hp = self.hpmax
            self.factory.broadOthers(self, color('cyan')+self.name+" has made level "+str(self.level)+color('white'))
            self.sendLine( "Experience to next level: "+str(int( (self.level*2 ** self.level)*.1 + self.level*70) ) )
            ach = choice(self.attacks)
            if randint(1,2) == 1:
                ach[1][1] += 1
                self.sendLine("Your "+ach[0] + " attack does more damage!")
            if randint(1,5) == 1:
                ach[1][0] += 1
                self.sendLine("Your "+ach[0] + " attack is phenominally better!")
            ach = choice(self.attacks)
            if randint(1,3) == 1:
                ach[1][1] += 1
                self.sendLine("Your "+ach[0] + " attack does more damage!")
            if randint(1,10) == 1:
                ach[1][0] += 1
                self.sendLine("Your "+ach[0] + " attack is phenominally better!")
            if self.level == 4:
                self.attacks.append( ['kick',[2,4]])
                self.sendLine("You have learned the kick attack!")
            if self.level == 8:
                self.attacks.append( ['uppercut',[1,15]])
                self.sendLine("You have learned the uppercut attack!")

##############################################
#           Player Commands                  #
##############################################

    def handle(self, line):
        #routes player commands to functions
        
        line = formatinput(line)
        ## did something so update idle time
        self.idletime = self.time
        
        splitline = line.lower().split(" ")
        
        #now we route the first command to a function
        fullmatches = ["quit"]
        partialmatches = ["who", "stop", "look", "kill", "go", "inventory", "get", "help", "chat", "say"]

        caught = 0
        
        if line == "":
            caught = 1 #just send status prompt
            
        if caught == 0:
            for entry in fullmatches:
                if entry == splitline[0]:
                    funct = eval("self."+entry)
                    funct( splitline )
                    caught = 1
                    break
            
        if caught == 0:
            for entry in partialmatches:
                if pMatch( splitline[0], entry):
                    funct = eval("self."+entry)
                    funct( splitline )
                    caught = 1
                    break

        if caught == 0:
            self.sendLine( "Unrecognized command: "+line )
            
        self.status()
    
    def close_connection(self):
        self.protocol.transport.loseConnection()
        try:
            self.factory.clientProtocols.remove( self.protocol )
        except:
            print "error removing connection" + str(self.protocol)
        

    def quit(self, args=[]):
        try:
            self.room.players.getself(self)
        except:
            print "error removing player from room on logout"
        try:
            self.factory.playerObjects.remove( self )
        except:
            print 'error removing player on logout'

        self.save()
        self.close_connection()
        self.factory.broadOthers(self, self.name+" has logged out.")
        del self

    def stop(self, args=[]):
        self.target = 0
        self.sendLine("You stop attacking.")
    
    def get(self, what=[]):
        what = what[1:]
        if what != []:
            thing = self.room.items.get(what)
            if thing:
                self.items.append( thing )
                room.sendinroom( self.name+" picks up the "+thing.name+".")
            else:
                self.sendLine("You don't see a " + what[0] + " here.")
            
    
    def inventory(self, args=[]):
        stuff = self.items.listcontents()
        if stuff == ".":
            self.sendLine ( "You don't have anything.")
        else:
            self.sendLine ( "You have: "+ stuff)

    
            
    def kill(self, args=[]):
        what = args[1:] #arg1 from splitline
        if what == []:
            self.sendLine("Kill what?")
        else:
            target = 0
            
            for entry in self.room.players:
                for item in entry.name.split(" "):
                    if pMatch( what[0], item ):
                        target = entry
            for entry in self.room.monsters:
                for item in entry.name.split(" "):
                    if pMatch( what[0], item ):
                        target = entry
            if target != 0:
                self.target = target
                self.room.sendinroom(self.name+" attacks the "+target.name)
        
       
    def say(self, args=[]):
        what = " ".join( args[1:] )
        if what != "":
            self.others( color("yellow") + self.name + color("white") + " says, '" + what + "'" )
            self.sendLine( "You say, '" + what + "'" )
        else:
            self.sendLine("Say what?")

    def chat(self, args=[]):
        what = " ".join( args[1:] )
        if what != "":
            self.factory.broadOthers(self, color("cyan") + self.name+": "+ what + color("white"))
        else:
            self.sendLine("Chat what?")
    
    def look(self, args=[]):
        what = args[1:]
 
        if what != []:
            target = 0
            for entry in self.room.players:
                if what[0] in entry.name:
                    target = entry
            for entry in self.room.monsters:
                if what[0] in entry.name:
                    target = entry
            if target != 0:
                for entry in target.desc:
                    self.sendLine( entry )
                    
        elif what == []:
            self.sendLine(" ")
            self.sendLine( color("cyan")+ self.room.name.center(80) )
            for entry in self.room.desc:
                self.sendLine( color("white")+ entry.center(80) )
            self.sendLine(" ")
            if self.room.exits != []:
                exits ="Exits: "
                for entry in self.room.exits:
                    exits = exits + entry[1] + ", "
                exits = exits[:-2] + "."
                self.sendLine( color("green")+ exits + color("white") )

            
            others = self.room.players.listcontents(self) #exclude arg
            if others != ".":
                self.sendLine( color("magenta")+ "You see: "+ others + color("white") )
            

            others = self.room.monsters.listcontents()
            if others != ".":
                self.sendLine( color("white")+ "You see: " + others + color("white") )

            stuff = self.room.items.listcontents()
            if stuff != ".":
                self.sendLine( "On the ground: "+stuff )
    
    

    def help(self, args=[]):
        self.sendLine( color('black')+"-----------------"+background('yellow')+"COMMANDS"+background('black')+"---------------"+color('white'))
        self.sendLine( "look   : look at the room, or at an object")
        self.sendLine( "get    : pick up an item")
        self.sendLine( "kill   : attack a player or monster")
        self.sendLine( "stop   : stop attacking")
        self.sendLine( "who    : list players with stats")
        self.sendLine( "go     : leave through an exit")
        self.sendLine( "chat   : broadcast a message to everyone in the game")
        self.sendLine( "say    : talk to people in your area")
        self.sendLine( "island : view information about the island")
        self.sendLine( "quit   : use this to "+color('cyan')+"save your game"+color('white'))
        self.sendLine( "-------------------------------------------------------------------")

    def who(self, args=[]):
        self.sendLine( color('magenta')+"NAME        LEVEL       EXP         KILLS       DEATHS      PEPPERS")
        self.sendLine(                  "-------------------------------------------------------------------"+color('white'))
        for entry in self.factory.clientProtocols:
            player = entry.player
            self.sendLine( player.name.ljust(12)+ str(player.level).ljust(12) +str(player.exp).ljust(12) +str(player.kills).ljust(12)+str(player.deaths).ljust(12)+str(player.items.count("pepper")).ljust(12) )

   


    
                                     
                
        
    
