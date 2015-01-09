from mud.core import *

verbs.register("kill", "kill|k|attack")
verbs.register_structure("kill", "{1}")

@check
@given("player", non("entity"))
def kill(a, b):
  say("You can't attack "+act("indefinate_name", b)+".")
  return False

@check
@given("player", undefined)
def kill(a, b):
  return False

@action
@given("player", "entity")
def kill(a, b):
  say("You attack ", act("indefinate_name", b)+".")

