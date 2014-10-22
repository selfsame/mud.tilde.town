from objects import *
from random import randint, choice
import copy
import os, sys

# mkdir -p in python, from:
# http://stackoverflow.com/questions/600268/mkdir-p-functionality-in-python
def mkdir_p(path):
  try:
    os.makedirs(path)
  except OSError as exc: # Python >2.5
    if exc.errno == errno.EEXIST:
      pass
    else:
      raise

def formatinput(raw):
    if raw.startswith('\xff'):
      raw = raw[3:]

    sp = repr(raw).split('\\x08')
    word = ""
    active = 0
    for i in range( len(sp) - 1 ):
        if sp[i] == '':
            sp[active] = sp[active][:-1]
        else:
            sp[i] = sp[i][:-1]
            active = i
        
    for entry in sp:
        word += entry
    
    return word[1:-1]

def pMatch(term1, term2):
    tl = len(term1)
    if term1.lower() == term2[:tl].lower():
        return 1    


def parseIslands(editpath, factory):
    islandlist = {}
    pathname = os.path.dirname(sys.argv[0]) + editpath[1:]
    for subdir, dirs, files in os.walk(pathname):
        for file in files:
            file = open(pathname+file)
            for line in file:
                line = line[:-1]
                
                if line[:1] == "I":
                    
                    #current = islandlist[ len( islandlist )-1 ]
                    
                    id = line.split(":")[1]
                    islandlist[ id ] = island() 
                    current = islandlist[ id ]
                    
                    current.name = line.split(":")[2]
                    
                if line[:1] == "V":
                    current.desc.append(  line.split(":")[1]  )
                    
                if line[:1] == "R":
                    id = line.split(":")[1]
                    
                    current.roomlist[ id ] = room(factory)
                    curroom = current.roomlist[ id ]
                    curroom.name = line.split(":")[2]
                    
                if line[:1] == "D":
                    curroom.desc.append(  line.split(":")[1]  )
                if line[:1] == "E":
                    curroom.exits.append(  [ line.split(":")[1]  , line.split(":")[2] ]  )
                        
                if line[:1] == "S":
                    sp = line.split(":")
                    curroom.spawn.append( [ int( sp[1]), [ int(sp[2].split('d')[0]), int(sp[2].split('d')[1]) ] ] )

            file.close()
            
    return islandlist


def parseMonsters(editpath):
    monsterlist = []
    pathname = os.path.dirname(sys.argv[0]) + editpath[1:]
    for subdir, dirs, files in os.walk(pathname):
        for file in files:
            file = open(pathname+file)
            for line in file:
                line = line[:-1]
                if line[:1] == "N":
                    monsterlist.append( monster() )
                    current = monsterlist[ len( monsterlist ) - 1 ]
                    current.id = line.split(":")[1]
                    current.name = line.split(":")[2]
                if line[:1] == "D":
                    current.desc.append(  line.split(":")[1]  )
                if line[:1] == "H":
                    current.hp = int( line.split(":")[1]  )
                if line[:1] == "A":
                    current.attacks.append( [ line.split(":")[1], [ int(line.split(":")[2].split('d')[0]),int(line.split(":")[2].split('d')[1])]])
                if line[:1] == "L":
                    current.level = int( line.split(":")[1]  )
                if line[:1] == "T":
                    #drops
                    current.drops.append( [ int(line.split(":")[1]), [ int(line.split(":")[2].split('d')[0]),int(line.split(":")[2].split('d')[1])]])

            file.close()
            
    return monsterlist

def parseItems(editpath):
    itemlist = []
    pathname = os.path.dirname(sys.argv[0]) + editpath[1:]
    for subdir, dirs, files in os.walk(pathname):
        for file in files:
            file = open(pathname+file)
            for line in file:
                line = line[:-1]
                if line[:1] == "N":
                    itemlist.append( item() )
                    current = itemlist[ len( itemlist ) - 1 ]
                    current.id = line.split(":")[1]
                    current.name = line.split(":")[2]
                if line[:1] == "D":
                    current.desc.append(  line.split(":")[1]  )
                if line[:1] == "V":
                    current.value = int( line.split(":")[1]  )
            file.close()
            
    return itemlist
