#!/usr/bin/env python
import pickle
import sys, os
import json
import player

def Mainold():
    result = {}
    peppers = {}
    for subdir, dirs, files in os.walk("mud.tilde.town/src/players"):
        for file in files:
            url = "mud.tilde.town/src/players/"+file
            pf = open(url, 'r')
            player =  pickle.load(pf)
            result[player.name] = player.exp
            peppers[player.name] = player.items.listcontents()
    s = sorted(result.items(), key=lambda x: x[1])
    s.reverse()
    print "<!DOCTYPE html><html><head></head>"
    print "<body>mud.tilde.town leaderboard<pre><code>"
    print "name             exp"
    print "==================="
    for t in s:
        print t[0]+"            "+str(t[1])+"       "+peppers[t[0]]
    print "</code></pre></body></html>"

def Main():
    print "<p>broke for the short term :(</p>"

if __name__== '__main__' :Main()
