from mud.core import *
from mud.core.util import *

bind.predicate("player", has("player"))
bind.predicate("fails", has("fails"))

def _is_client(e):
  try: return e.__name__ == "MUDClient"
  except: return False

bind.predicate("MUDClient", _is_client)

@serialize
def player(e):
  return True



@given("MUDClient", dictionary)
def player_enter_game(a, b):
  if GET(data.instances, GET(b, "uuid")):
    return call("reconnect", GET(data.instances, GET(b, "uuid")), a)
  default = data.instance("player", False)
  b = components._deserialize(b)
  b['player'] = a
  new = components._merge([default, b])
  data.subject = new
  data.register(new)
  call("player_init", new)
  return new



@given("player", "MUDClient")
def reconnect(a, b):
  print "reconnecting "+name(a)
  GET(a, "player").close_connection("reconnecting")
  a["player"] = b
  return a


@given("player")
def player_init(e):
  r = util.location(e)
  r['contents'].append(e['uuid'])
  dispatch.stack("init", e)

@before(a(non("located"), "player"))
def player_init(e):
  e['located'] = "lobby"

@after("player")
def player_init(e):
  call("enact", e, "broadcast", "{#magenta}{#bold}"+e["firstname"]+" has entered the game.{#reset}")
  call("player_input", e, "look")



@given("player")
def get_client(e):
  return e["player"]

@given("player")
def line_prompt(a):
  if a["player"].dialogue: return ""
  h = colors.special["heart"]
  hp = int(a["living"]["hp"])
  maxhp = int(a["living"]["hpmax"])
  return parse.template("{#bold}{#red}"+h+"{#yellow}"+str(hp)+"{#green}/"+str(maxhp)+"{#resetall}:")

@given("player")
def quit(a):
  call("save", a)
  call("enact", a, "broadcast", "{#magenta}"+a["firstname"]+" has disconnected.{#reset}")
  call("delete", a)
  call("get_client", a).close_connection("QUITTING!")

  


@given("player")
def save(a):
  ser = components._serialize(a)
  try:
    idx = a["player"].character_idx
    a["player"].account["characters"][idx] = ser
    a["player"].save()
    say("{#magenta}GAME SAVED{#reset}")
  except:
    say("{#red}{%white}ERROR SAVE ERROR{#reset}")


@given(verb, "player", sequential)
def object_blocked(v, p, args):
  res = filter(string, map_get_in(["fails", v], args))
  if res:
    say(res[0])
    return True


