from mud.core.actions import *
from standard.predicates import *
from mud.core import verbs

verbs.register("write", "write|inscribe", {"past":"wrote"})
verbs.register_structure("write", "{1:text}on|in{2}","{1:text}on|in{2}with|using{3}")

verbs.register("erase", "erase", {"progressive":"erasing"})
verbs.register_structure("erase", "{1}with{2}")

implement = a("implement")
surface = a("surface")
def written(e):
	if "writing" in e:
		return e["writing"] not in ["", False]
	return False
blank = non(written)


@check
@given(player, string, non(surface), implement)
def write(a, b, c, d):
  say("You try to write on "+act("indefinate_name", c)+" but your "+act("printed_name", d)+" doesn't leave a mark.")
  return False

@before
@given(player, string, surface, implement)
def write(a, b, c, d):
  say("You start writing '"+b+"' on "+act("indefinate_name", c)+".")

@action
@given(player, string, surface, implement)
def write(a, b, c, d):
  c["writing"] = "\r\n"+b


@before
@given(a(blank, surface))
def printed_name(e):
  return "blank "


@after
@given(player, a(written, surface))
def look(a, b):
  say("It reads:\r\n"+str(b.get("writing"))+"\r\n")










