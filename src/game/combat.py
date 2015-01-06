from required import *
from predicates import *

verbs.register("kill", "kill|k|attack")
verbs.register_structure("kill", "{1}")

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


print "combat.py"


import sys
import re
import verbs
for k in sys.modules.keys():
	if "verbs" in k:
		print "("+k+")"