import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from actions.core import *
from util import *
from predicates import *
import verbs

verbs.register("write", "write|inscribe")
verbs.register_structure("write", "{1:text}on|in{2}")

@check
@given(player, string, non(entity))
def write(a, b, c):
  say("You write '"+b+"' on "+act("indefinate_name", c)+".")
  return True















