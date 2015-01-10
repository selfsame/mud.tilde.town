from mud.core import *
from colors import color

player = has("player")

predicates.register("player", has("player"))
predicates.register("fails", has("fails"))

@serialize
def player(e):
  return True



@action
@given(verb, "player", sequential)
def object_blocked(v, p, args):
  res = filter(string, map_get_in(["fails", v], args))
  if res:
    say(res[0])
    return True



@action
@given("player")
def line_prompt(a):
  h = colors.special["heart"]
  hp = a["living"]["hp"]
  maxhp = a["living"]["hpmax"]
  return parse.template("{#bold}{#red}"+h+"{#yellow}"+str(hp)+"{#green}/"+str(maxhp)+"{#reset}:")

@action
@given("player")
def quit(a):
  print "quit(player)"
  act("save", a)
  player_inst = a.get("player")
  player_inst.quit()


@action
@given("player")
def save(a):
  print "save(player)"
  ser = components._serialize(a)
  if a["player"].save(ser):
    say("{#magenta}GAME SAVED{#reset}")
  else:
    say("{#red}{%white}ERROR SAVE ERROR{#reset}")

@action
@given("player", string)
def talk(a, b):
  say("You say '{#yellow}"+b+"{#reset}'.")
  report_to(location(a), name(a)+" says: ""{#yellow}"+b+"{#reset}")

@action
@given("player", string, "entity")
def talk(a, b, c):
  message = "'{#yellow}"+b+"{#reset}' to "+act("indefinate_name", c)+"."
  say("You say "+message)
  report_to(location(a), name(a)+" says "+message)


@action
@given("player")
def printed_name(a):
  n = str(the(a, "firstname"))
  return "{#magenta}"+n+"{#reset}"


@after
@given("player", anything)
def walk(a, b):
  act("look", a)


@action
@given("player", string)
def walk(a, b):
  loc = location(a)
  exits = the(loc, "exits")
  for k in exits:
    if b == k:
      v = exits[k]
      r = data.rooms.get(v)
      if act("move", a, r):
        act("leave", loc, a, k)
        act("arrive", a, r)


@action
@given("player", "thing")
def get_name(a,b):
  return (the(b, "name") or the(b, "id") or "thing")

@action
@given("player", "thing", equals("name"))
def printing(actor, subjects, property):
  res = dict_act("get_name", actor, subjects)
  s = ""
  if res.get("before"): s += res.get("before")
  s += res.get("action") or "thing"
  if res.get("after"): s += res.get("after")
  return s
  


@after
@given("player", "thing")
def get_name(a,b):
  return "(named)"  


@action
@given("player")
def look(a):
  r = location(a)
  act("describe", a, r)


@action
@given("player", undefined)
def look(a, b):
  say("you dont see anything like that here.")


@action
@given("player", "thing")
def look(a, b):
  relation = act("scope_relation", b, a)
  say("you look at ", act("indefinate_name", b)+relation+".\r\n", act("write",b,'desc'))


@check
@given("player", a("fixed", "object"))
def take(a, b):
  say("You try, but it seems to be permamently attached.")
  return False

@check
@given("player", a(non("object"), "entity"))
def take(a, b):
  say("Maybe if it was unconscious, or dead..")
  return False

@action
@given("player", anything)
def take(a, b):
  say("That's not something you could take.")

@action
@given("player", a("located", "object"))
def take(a, b):
  relation = act("scope_relation", b, a)
  if act("move", b, a):
    say("you pick up the ", name(b)+relation+".\r\n")
    report_to(location(a), act("indefinate_name", a), "picks up the", name(b)+relation+".\r\n")


@after
@given("entity", "thing")
def look(a, b):
  relation = act("scope_relation", b, a)
  report_to(location(a), act("indefinate_name", a), "looks at", act("indefinate_name", b)+relation+".")

@action
@given("player")
def inventory(a):
  say("You have "+ act("list_contents", a, a) + ".\r\n")

@action
@given("player", a("located"))
def drop(a, b):
  if act("move", b, location(a)):
    say("you drop the ", name(b)+".\r\n")
    report_to(location(a), act("indefinate_name", a), "drops the", name(b)+".\r\n")

@check
@given("player", a("located"), a("closed", "container"))
def drop(a, b, c):
  if act("open", a, c):
    return True
  say("You're not able to open it.")
  return False

@action
@given("player", a("located"), "container")
def drop(a, b, c):
  p = path(c)
  print "PATH", map(name, map(from_uid, p))
  if b["uuid"] in p or b["id"] in p:
    say("you can't put something inside of itself.")
    return False
  if act("move", b, c):
    relation = act("scope_relation", c, a)
    say("you put the ", name(b)+" into "+act("indefinate_name", c)+relation+".\r\n")
    report_to(location(a), act("indefinate_name", a), "puts the ", name(b)+" into "+act("indefinate_name", c)+relation+".\r\n")




