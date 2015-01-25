from mud.core import *

bind.verb("write", "write|inscribe", {"past":"wrote", "doc":"writes text on appropriate surface with a writing implement."})
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
  say("Your "+call("printed_name", d)+" doesn't leave a mark.")
  return False

@before("player", string, "surface", "implement")
def write(a, b, c, d):
  report("[Subject] [verb] on [second object] with [third object].")

@given("player", string, "surface", "implement")
def write(a, b, c, d):
  c["writing"] = "\r\n"+b


@before(a("blank", "surface"))
def printed_name(e):
  return "blank "


@after("player", a("written", "surface"))
def look(a, b):
  say("It reads:\r\n"+str(b.get("writing"))+"\r\n")










