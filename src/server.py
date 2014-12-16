#!/usr/bin/env python

import sys
from twisted.internet import reactor, task
from twisted.internet.protocol import ServerFactory
from twisted.protocols.basic import LineOnlyReceiver

import dialogue as d
import time
from intro import Intro
import parse
import data
from game import *
from actions import *

class MUDProtocol(LineOnlyReceiver):
    ## Connection object, will be hooked up to player object
    def __init__(self):
        self.player = False
        self.account = False
        self.character_idx = 0
        self.idle = 0

    def echo(self, mode):
        if mode == False:
          self.transport.write('\xff\xfb\x01')
        else:
          self.transport.write('\xff\xfc\x01')

    def clear(self):
        self.transport.write('\033[2J')

    def close_connection(self, message="disconnecting"):
        self.sendLine(message)
        self.transport.loseConnection()
        del self
        
    def save(self):
        if self.account:
          path = './players/'+self.account['name']+'.json'
          return components.make.save_json(self.account, path)
    
    def add_dialogue(self, dialogue):
        self.dialogue = dialogue
        res = dialogue.initial()
        if isinstance(res, (str, unicode)):
                self.sendLine(res)

    def lineReceived(self, l):
        self.idle = 0
        line = parse.strip_escape_chars(l)
        if self.dialogue:
            res = self.dialogue.input(line)
            if res == False or self.dialogue.done == True:
                self.dialogue = False
            if isinstance(res, (str, unicode)):
                self.sendLine(res)
        elif self.player:
            self.player.input(line)
            self.player.prompt()

    def sendLine(self, line):
        self.transport.write(line+"\r\n")

    def connectionMade(self):
        self.factory.clientProtocols.append(self)
        self.add_dialogue(Intro(self))
    
    def update(self, delta):
      self.idle += delta
      if self.player:
        self.player.update(delta)
      if self.idle > 800:
        if self.player:
            self.idle = 300
            self.player._quit()
        self.close_connection("timed out")


  
    def enter_game(self, idx):
        self.character_idx = idx
        self.player = Player(self, self.account["characters"][idx])
        self.factory.broadcast(data['firstname']+" has entered the game")


class ChatProtocolFactory(ServerFactory):

    protocol = MUDProtocol

    def __init__(self):
        self.clientProtocols = []
        self.last_time = time.time()
        loopingCall = task.LoopingCall(self.timeDisbatch)
        loopingCall.start(.5)

    def broadcast(self, mesg):
        #This should go to any state client
        for client in self.clientProtocols:
            client.sendLine(mesg)

    def broadOthers(self, me, mesg):
        #This should send to all playerobjects, so no spam to login
        for client in self.playerObjects:
            if client != me:
                client.sendLine(mesg)

    def timeDisbatch(self):
        delta = time.time() - self.last_time
        self.last_time = time.time()
        for client in self.clientProtocols:
          client.update(delta)
        data.game.update(delta)
        return True

def Main():
    port = 5071
    if len(sys.argv) > 1: 
        port = int(sys.argv[1])
    print "Starting mud.tilde.town server"
    data.game = Game()
    factory = ChatProtocolFactory()
    reactor.listenTCP(port, factory)
    reactor.run()

if __name__== '__main__' :Main()
