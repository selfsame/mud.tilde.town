import os
from functions import formatinput
from colors import *
from player import player
import pickle
import time
import hashlib
import binascii

IAC_WONT_ECHO = '\xff\xfc\x01'
IAC_WILL_ECHO = '\xff\xfb\x01'

def verify(hash, plaintext):
  if hash == hashlib.sha512(plaintext).hexdigest():
    return True
  else:
    return False

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
                    self.transport.write("(typing will be hidden)>")
                    self.transport.write(IAC_WILL_ECHO)
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
                    self.transport.write("(typing will be hidden)>")
                    self.transport.write(IAC_WILL_ECHO)
                    self.status = 1
                except:
                    self.new = 1
                    self.sendLine("NEW CHARACTER: What is your password?")
                    self.transport.write("(typing will be hidden)>")
                    self.transport.write(IAC_WILL_ECHO)
                    self.status = 1
                
        
    elif self.status == 1: #was asked for password
        safePass = formatinput(line)
        # Stop hiding input
        self.sendLine('')
        self.transport.write(IAC_WONT_ECHO)
        
        if self.dopple == 1:
            if verify(self.player.password, self.player.salt + safePass):
                # delete other protocol and player reference, tell player object this is its protocol
                self.status = 4
                self.sendLine("Login successful! (press enter)")
                self.player.protocol = self
                for entry in self.factory.clientProtocols:
                    if entry.player == self.player and entry != self:
                        del self.factory.clientProtocols[ self.factory.clientProtocols.index(entry) ]          
            else:
              self.sendLine(color("red")+"Incorrect password."+color("white"))
              self.player.close_connection()
              del self.player

        elif self.new == 0: #not new
            if verify(self.player.password, self.player.salt + safePass):
                self.status = 4     
                self.sendLine("Login successful! (press enter)")
            else:
                self.sendLine(color("red")+"Incorrect password."+color("white"))
                self.player.close_connection()
                del self.player
                
        elif len( safePass ) > 2: #making a new password #new == 1
            self.player = player(self, self.factory, time.time() )
            self.player.salt = os.urandom(16)
            self.player.password = hashlib.sha512(self.player.salt + safePass).hexdigest()
            self.player.name = self.name
            self.status = 3
            self.sendLine("What is your sex (m/f/o):") ## Move me
        else:
            self.sendLine("Too short, try again:")
            self.transport.write(">")

            
    if self.status == 2: #Skipping status 3 for creation
        if self.new == 0:
            self.status = 4
        
