from mud.core.actions import *
from mud.core import verbs
from mud.core.components import instance, register
from mud.core.util import location, name
from mud.core.predicates import equals, string, registry, get

verbs.register("admin", "@")
verbs.register_structure("admin", "{1:text}","{1:text} {2}")
verbs.register_structure("admin", "{1:text} \"{2:text}\"")
verbs.register_structure("admin", "{1:text} {2} {3:text}={4:text}")



@action
@given("player", equals("show"), "thing")
def admin(a, b, c):
	res = []
	for k in c:
		res.append("{#yellow}"+str(k)+":"+"{#reset}"+str(c[k]))
	say("\r\n".join(res))

@action
@given("player", equals("predicates"), "thing")
def admin(a, b, c):
	res = []
	for k in registry:
		print k
		if get(k)(c): 
			col = "{#green}"
		else:
			col = "{#red}" 
		say(col+k+"{#reset}")


@action
@given("player", equals("instance"), string)
def admin(a, b, c):
	n = instance(c)
	register(n)
	say("You conjure up a "+name(n))
	act("move", n, location(a))
	act("arrive", n, location(a))

@action
@given("player", equals("set"), "thing", string, string)
def admin(a, b, c, d, e):
	val = e
	if e in ["true", "True"]:
		val = True
	if e in ["false", "False"]:
		val = False
	try:
		val = int(e)
	except:
		pass
	c[d] = val
	say(name(c)+"["+d+"] set to "+e)





