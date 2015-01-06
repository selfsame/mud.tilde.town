import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from components import load
from actions import *
from player import *
from standard import *


class Game():
  def __init__(self):
    load(os.sep.join(['./edit']))
    act("init")

  def update(self,delta):
    act("update", delta)













