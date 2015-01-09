from mud.core.actions import *
from mud.core.util import *
from mud.game.standard.predicates import *
from mud.core.colors import *
from mud.core import verbs, components, predicates
from mud.core.components import *
import random

def player(e):
  if dictionary(e) and e.get("player"): return True
  return False

predicates.register("player", has("player"))

@serialize
def player(e):
  return True



@action
@given(verb, "player", undefined)
def player_command(v, p, u):
  say("I can't understand what you are "+verbs.forms[v]["progressive"]+".")

@action
@given(verb, "player", undefined, "thing")
def player_command(v, p, u, a):
  say("I can't understand what you are "+verbs.forms[v]["progressive"]+" in the "+name(a)+".")


@action
@given("player")
def line_prompt(a):
  h = special["heart"]
  hp = a["living"]["hp"]
  maxhp = a["living"]["hpmax"]
  return color("red")+h+color("bold")+color("yellow")+str(hp)+"/"+color("reset")+str(maxhp)+color("cyan")+">"+color("reset")

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


@before
@given("player", "room")
def describe(p, r):
  say("\r\n{#cyan}    ~ ~ "+act("write",r,'name')+"{#cyan} ~ ~{#reset}\r\n ")

@action
@given("player", "room")
def describe(p, r):
  res = [act("write",r,'desc')," ",
    "You see "+ act("list_contents", p, r)+ ".",
    " ",
    "exits: {#yellow}{#bold}"+", ".join(the(r, 'exits').keys()) + "{#reset}"," "]
  say("\r\n".join(res))


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


@action
@given("player", "holder")
def list_contents(a, b):
  conts = the(b, 'contents')
  #if the(a, 'uuid') in conts: conts.remove(the(a, 'uuid'))
  names = {}
  kinds = {}
  for item in conts:
    ent = from_uid(item)
    if ent == a:
      break
    n = act("printed_name", ent)
    if names.get(n):
      names[n] += 1
    else:
      names[n] = 1
    if not kinds.get(n):
      kinds[n] = from_uid(item)
  res = []
  for k in names:
    if names[k] > 1:
      r = "".join(act("indefinate_name", names[k], kinds[k]))
    else:
      r = "".join(act_stack("indefinate_name", kinds[k]))
    if r: res.append( str(r) )
  if len(res) == 0:
    res = ["nothing"]
  lastpair = res[-2:]
  prev = res[:-2] + [" and ".join(lastpair)]
  return ", ".join(prev)



@action
@given("holder")
def list_contents(b):
  conts = the(b, 'contents')
  names = {}
  kinds = {}
  for item in conts:
    ent = from_uid(item)
    n = act("printed_name", ent)
    if names.get(n):
      names[n] += 1
    else:
      names[n] = 1
    if not kinds.get(n):
      kinds[n] = from_uid(item)
  res = []
  for k in names:
    if names[k] > 1:
      r = "".join(act("indefinate_name", names[k], kinds[k]))
    else:
      r = "".join(act_stack("indefinate_name", kinds[k]))
    if r: res.append( str(r) )
  lastpair = res[-2:]
  prev = res[:-2] + [" and ".join(lastpair)]
  return ", ".join(prev)


