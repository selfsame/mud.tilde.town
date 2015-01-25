from mud.core import *
from mud.core.CAPSMODE import *

bind.verb("chat", "chat|[\;]", {"past":"chatted", "doc":"Sends text to all players."})
bind.verb_pattern("chat", "{1:text}")

bind.verb("history", "history", {"doc":"Prints the chat history, can optionally be given number of lines to recall."})

data.game["history"] = []

@given("player", string)
def broadcast(a, b):
	data.game["history"].append(b)
	data.game["history"] = data.game["history"][-60:]
	report(b)

@given("player")
def history(a):
	for m in data.game["history"][-20:]:
		say(m)

@given("player", string)
def history(a,s):
	try: s = int(s)
	except: s = 20
	for m in data.game["history"][s * -1:]:
		say(m)

@given("player", string)
def chat(a, b):
	message = "{#cyan}{#bold}"+GET(a, "firstname")+" "+GET(a, "lastname")+" : {#reset}{#cyan}"+b+"{#reset}"
	call("enact", a, "broadcast", message)

@given("entity", equals("broadcast"))
def understood_scope_while(e, v): 
  clients = e["player"].factory.clientProtocols
  return filter(lambda x: x not in [False, None], map(lambda x: x.player, clients))



