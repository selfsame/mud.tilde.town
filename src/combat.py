from random import randint, choice
from colors import *

def attack(entity1, entity2, room):
    attack = choice(entity1.attacks)
    damage = 0
    for i in range(attack[1][0]):
        damage += randint( 1, attack[1][1])
    

    try:
        entity2.logged
        play = ""
    except:
        play = "the "

    of = randint(1, entity1.level*12)
    df = randint(1, entity2.level*12)

    if of >= df:   
        room.sendinroom( color("red")+entity1.name+" "+attack[0]+"s "+play+entity2.name+" for "+str(damage)+"!"+color("white"))
        entity2.hurt(entity1, damage)
    else:
        room.sendinroom( color("blue")+entity1.name+" misses "+play+entity2.name+"!"+color("white"))
    for entry in room.players:
        entry.status()
    
