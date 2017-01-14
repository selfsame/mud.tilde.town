#!/usr/bin/env python
import sys, os, time, socket

from mud.login import Intro
from mud.core import *
from mud.game import *


host = '127.0.0.1'
port = 5071
if len(sys.argv) > 1: 
    port = int(sys.argv[1])
clients = []

class telnetServer():
    def __init__(self, (socket, address)):
        self.socket = socket
        self.address = address

    def run(self):
        clients.append(self)
        print '%s:%s connected.' % self.address
        while True:
            data = self.socket.recv(1024)
            if not data:
                break
            for c in clients:
                c.socket.send(data)
        self.socket.close()
        print '%s:%s disconnected.' % self.address
        clients.remove(self)

def Main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((host, port))
    s.listen(4)
    print("bound server to "+str(host)+":"+str(port))
    data.load(os.sep.join(['./mud/game']))
    call("init")
    while True:
        telnetServer(s.accept()).run()

if __name__== '__main__' :Main()
