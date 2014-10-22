from functions import formatinput
from colors import *
from player import player
import pickle
import time

def login(self, line): #self is the protocol object
    line = formatinput(line)
    splitline = line.lower().split(" ")
    
    if self.status == 0: #was asked for name
        safeName = formatinput(line)
        
        if len(safeName) <= 2 or len(safeName) >= 12:
            self.sendLine("must be 3 to 12 characters, try again:")
            self.transport.write(">")
            
        elif safeName.lower() in ['look', 'get', 'kill', 'kil','loo', 'who', 'help']:
                self.sendLine("illegal name, try again:")
                self.transport.write(">")
                
        else:
            self.name = safeName
            
            for entry in self.factory.playerObjects: #allready logged in?
                if safeName == entry.name:
                    self.player = entry #go ahead and assume that player, the check for password is below
                    self.sendLine("Enter your password (re-login):")
                    self.transport.write(">")
                    self.dopple = 1
                    self.status = 1
     
            if self.dopple == 0:
                
                #make sure player isn't allready loaded
                #try to load character
                
                try:
                    savefile = open('./players/'+self.name+'.sav', 'r') #load player object
                    self.player = pickle.load(savefile)
                    self.player.protocol = self
                    self.player.factory = self.factory
                    self.player.time = time.time()
                    self.player.idletime = time.time()
                    self.player.islands = self.factory.islands
                    savefile.close()
                    self.sendLine("What is your password?")
                    self.transport.write(">")
                    self.status = 1
                except:
                    self.new = 1
                    self.sendLine("NEW CHARACTER: What is your password?")
                    self.transport.write(">")
                    self.status = 1
                
        
    elif self.status == 1: #was asked for password
        safePass = formatinput(line)
        
        if self.dopple == 1:
            if self.player.password == safePass:
                # delete other protocol and player reference, tell player object this is its protocol
                self.status = 2
                self.sendLine("Login successful!")
                self.player.protocol = self
                for entry in self.factory.clientProtocols:
                    if entry.player == self.player and entry != self:
                        del self.factory.clientProtocols[ self.factory.clientProtocols.index(entry) ]          
                
        elif self.new == 0: #not new
            if self.player.password == safePass:
                self.status = 2
                
                self.sendLine("Login successful!")
            else:
                self.sendLine(color("red")+"Incorrect password."+color("white"))
                self.status = 0
                self.sendLine("Enter your name:")
                self.transport.write(">")
                del self.player
                
        elif len( safePass ) > 2: #making a new password #new == 1
            self.player = player(self, self.factory, time.time() )
            self.player.password = safePass
            self.player.name = self.name
            self.status = 3
            self.sendLine("What is your sex (m/f/o):") ## Move me
        else:
            self.sendLine("Too short, try again:")
            self.transport.write(">")

            
    if self.status == 2: #Skipping status 3 for creation
        if self.new == 0:
            self.status = 4
        
