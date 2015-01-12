from mud.core import *

bind.verb("write", "write|inscribe", {"past":"wrote"})
bind.verb_pattern("write", "{1:text}on|in{2}","{1:text}on|in{2}with|using{3}")

bind.verb("erase", "erase", {"progressive":"erasing"})
bind.verb_pattern("erase", "{1}with{2}")

def written(e):
	if has("writing")(e):
		return e["writing"] not in ["", False]
	return False

bind.predicate("surface", has("surface"))
bind.predicate("implement", has("implement"))

bind.predicate("written", written)
bind.predicate("blank", non(written))

@check("player", string, non("surface"), "implement")
def write(a, b, c, d):
  say("You try to write on "+call("indefinate_name", c)+" but your "+call("printed_name", d)+" doesn't leave a mark.")
  return False

@before("player", string, "surface", "implement")
def write(a, b, c, d):
  say("You start writing '"+b+"' on "+call("indefinate_name", c)+".")

@given("player", string, "surface", "implement")
def write(a, b, c, d):
  c["writing"] = "\r\n"+b


@before(a("blank", "surface"))
def printed_name(e):
  return "blank "


@after("player", a("written", "surface"))
def look(a, b):
  say("It reads:\r\n"+str(b.get("writing"))+"\r\n")










