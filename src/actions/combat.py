import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from core import *
from util import *
from predicates import *
import random
from parse import table_choice

verbs.register("kill", "kill|k|attack")

@check
@given(player, non(entity))
def kill(a, b):
  say("You can't attack "+act("indefinate_name", b)+".")
  return False

@check
@given(player, undefined)
def kill(a, b):
  return False

@action
@given(player, entity)
def kill(a, b):
  say("You attack ", act("indefinate_name", b)+".")