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
  default = data.instance("player", False)
  b['player'] = a
  new = dict(default.items() + b.items())
  data.subject = new
  data.register(new)
  call("player_init", new)
  return new


@given("player")
def player_init(e):
  recursive_register(e)
  r = util.location(e)
  r['contents'].append(e['uuid'])
  call("init", e)

@before(a(non("located"), "player"))
def player_init(e):
  e['located'] = "lobby"

@after("player")
def player_init(e):
  call("player_input", e, "look")

def recursive_register(e):
  if isinstance(e, str): return e
  cont = e.get("contents")
  if cont:
    e["contents"] = map(recursive_register, cont)
  data.register(e)
  return e.get("uuid")


@given("player")
def get_client(e):
  return e["player"]

@given("player")
def line_prompt(a):
  if a["player"].dialogue: return ""
  h = colors.special["heart"]
  hp = a["living"]["hp"]
  maxhp = a["living"]["hpmax"]
  return parse.template("{#bold}{#red}"+h+"{#yellow}"+str(hp)+"{#green}/"+str(maxhp)+"{#reset}:")

@given("player")
def quit(a):
  call("save", a)
  call("delete", a)
  call("get_client", a).close_connection("QUITTING!")

  


@given("player")
def save(a):
  ser = components._serialize(a)
  try:
    idx = a["player"].character_idx
    a["player"].account["characters"][idx] = character
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


