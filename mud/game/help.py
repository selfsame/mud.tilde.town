from mud.core import *
from mud.core.CAPSMODE import *

bind.verb("help", "help", {"doc":"Help helps."})
bind.verb_pattern("help", "{1:text}")


concepts = {
    "kinds":"Objects in the game can be refered to by 'kinds'.\r\nexample: 'get weapon'",
	"containment":
	"When giving commands, you can refer to specific contained things.\r\nexample:{#yellow} 'get the coin in the leather bag inside of the chest.'",
	"plurality":"You can refer to plural groups of things by using a plural form of a kind.\r\nexample:{#yellow} 'objects', 'weapons', 'containers', 'women', 'books.'",
	"adjectives":"adjectives can be used to filter the object/s you mean.\r\nexample:{#yellow} 'put leather clothing in the red bag', 'look at unarmed men.'"
}

@given("player")
def help(a):
	message = [
	"{#bold}",
	"{#white}HELP MENU - for more information, type - 'help [topic]'",
	"\r\n-----------------------------------{#green}COMMANDS{#white}------------------------------------"]
	coms = "{#cyan}"
	for k in verbs.forms:
		coms += k+" "
	message.append(coms)
	message += [
	"\r\n{#white}-----------------------------------{#green}CONCEPTS{#white}------------------------------------",

	"{#yellow}containment kinds plurality adjectives\r\n"]

	say("\r\n".join(message))



@given("player", string)
def help(a, s):
	if s in verbs.structures:
		doc = GET_IN(verbs.forms, [s, "doc"])
		say("\r\n{#bold}{#green}"+s+"{#white} ("+str(verbs.regexverbs[s])+")")
		if doc: say(doc)
		say("{#cyan}forms:{#white}")
		for struct in verbs.structures[s]:
			n = struct.replace("{", "<").replace("}", ">").replace("<", "{#cyan}<").replace(">", ">{#white}")
			n = n.replace("|", "{#red}|{#white}")
			n = n.replace("*", "{#red}*{#white}")
			n = n.replace("?", "{#red}?{#white}")
			n = n.replace("+", "{#red}+{#white}")
			n = n.replace("\{#red}?{#white}", "\?")
			n = n.replace("\{#red}*{#white}", "\*")
			n = n.replace("\{#red}|{#white}", "\|")
			n = n.replace("\{#red}+{#white}", "\+")
			say(" - {#green}"+s+"{#white} "+n)

	elif s in concepts:
		say(str(concepts[s]))
		if s == "adjectives":
			say("\r\nimplemented:\r\n{#cyan}  "+", ".join(bind._adjectives.keys()))
		elif s == "kinds":
			say("\r\nimplemented:\r\n{#cyan}  "+", ".join(bind._kinds.keys()))
	else:
		say("no information.")
	say("\r\n")

