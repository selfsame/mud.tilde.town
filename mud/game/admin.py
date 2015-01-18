from mud.core import *
from mud.core.util import location, name


bind.verb("admin", "@")
bind.verb_pattern("admin", "{1:text}","{1:text} {2}")
bind.verb_pattern("admin", "{1:text} \"{2:text}\"")
bind.verb_pattern("admin", "{1:text} {2} {3:text}={4:text}")



@given("player", equals("show"), "thing")
def admin(a, b, c):
	res = []
	for k in c:
		res.append("{#yellow}"+str(k)+":"+"{#reset}"+str(c[k]))
	say("\r\n".join(res))

@given("player", equals("delete"), "thing")
def admin(a, b, c):
	try:
		call("delete", n)
		say("deleted!")
	except:
		say("delete failed.")

@given("player", equals("show"))
def admin(a, b):
	res = []
	for k in a:
		res.append("{#yellow}"+str(k)+":"+"{#reset}"+str(a[k]))
	say("\r\n".join(res))

@given("player", equals("predicates"), "thing")
def admin(a, b, c):
	res = []
	for k in predicates._registry:
		print k
		if predicates._get(k)(c): 
			col = "{#green}"
		else:
			col = "{#red}" 
		say(col+k+"{#reset}")

@given("player", equals("instance"), string)
def admin(a, b, c):
	n = data.instance(c)
	say("You conjure up a "+name(n))
	call("move", n, location(a))
	call("arrive", n, location(a))

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

@given("player", equals("room"))
def admin(a, b):
	a["player"].add_dialogue(RoomBuilder(a))


class RoomBuilder(Dialogue):
	def initial(self):
		self.__name__ = "RoomBuilder"
		self.con["player"].clear()
		return "ROOM CREATION\r\nquit new"

	def start(self, s):
		if s == "quit": return False
		if s == "new": return "ENTER ROOM IDENTIFIER:"
		self.state = self.name
		return "[not a menu option]"

	def name(self, s):
		return False


@given("player", equals("colors"))
def admin(a, b):
	hues = ["black", "white", "yellow", "red", "magenta", "blue", "cyan", "green"]
	res = "{#reset}{%reset}default text\r\n"
	for b in hues:
		for weight in ["", "{#bold}"]:
			for c in hues:
				res += weight+"  {%"+b+"}{#"+c+"}"+colors.special["heart"]+str(" "+c+"     ")[0:6]+"{#reset}{%reset}"
			res += "\r\n"
		res += "\r\n"
	res += "\r\n"
	res += " ".join(colors.special.values())
	say(res)
