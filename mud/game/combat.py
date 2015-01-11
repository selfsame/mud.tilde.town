from mud.core import *

bind.verb("kill", "kill|k|attack")
bind.verb_pattern("kill", "{1}")

@check("player", non("entity"))
def kill(a, b):
  say("You can't attack "+call("indefinate_name", b)+".")
  return False

@check("player", undefined)
def kill(a, b):
  return False

@given("player", "entity")
def kill(a, b):
  say("You attack ", call("indefinate_name", b)+".")

