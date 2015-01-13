from mud.core import *
from colors import color
from mud.core.util import *


@given("player", string)
def talk(a, b):
  say("You say '{#yellow}"+b+"{#reset}'.")
  report_to(location(a), name(a)+" says: ""{#yellow}"+b+"{#reset}")

@given("player", string, "entity")
def talk(a, b, c):
  message = "'{#yellow}"+b+"{#reset}' to "+call("indefinate_name", c)+"."
  say("You say "+message)
  report_to(location(a), name(a)+" says "+message)

@given("player")
def printed_name(a):
  n = str(the(a, "firstname"))
  return "{#magenta}"+n+"{#reset}"


@after("player", anything)
def walk(a, b):
  call("look", a)


@given("player", string)
def walk(a, b):
  loc = location(a)
  exits = the(loc, "exits")
  for k in exits:
    if b == k:
      v = exits[k]
      r = data.rooms.get(v)
      if call("move", a, r):
        call("leave", loc, a, k)
        call("arrive", a, r)


@given("player", "thing")
def get_name(a,b):
  return (the(b, "name") or the(b, "id") or "thing")

@given("player", "thing", equals("name"))
def printing(actor, subjects, property):
  res = dict_call("get_name", actor, subjects)
  s = ""
  if res.get("before"): s += res.get("before")
  s += res.get("action") or "thing"
  if res.get("after"): s += res.get("after")
  return s 

@given("player", "thing")
def get_name(a,b):
  return "(named)"  

@given("player")
def look(a):
  r = location(a)
  call("describe", a, r)


@given("player", undefined)
def look(a, b):
  say("you dont see anything like that here.")


@given("entity", "thing")
def look(a, b):
  relation = call("scope_relation", b, a)
  report_to(location(a), call("indefinate_name", a), "looks at", call("indefinate_name", b)+relation+".")

@given("player", "thing")
def look(a, b):
  relation = call("scope_relation", b, a)
  say("you look at ", call("indefinate_name", b)+str(relation)+".\r\n", call("write",b,'desc'))

@check("player", a("fixed", "object"))
def take(a, b):
  say("You try, but it seems to be permamently attached.")
  return False

@check("player", a(non("object"), "entity"))
def take(a, b):
  say("Maybe if it was unconscious, or dead..")
  return False

@given("player", anything)
def take(a, b):
  say("That's not something you could take.")

@given("player", a("located", "object"))
def take(a, b):
  relation = call("scope_relation", b, a)
  if call("move", b, a):
    say("you pick up the ", name(b)+relation+".\r\n")
    report_to(location(a), call("indefinate_name", a), "picks up the", name(b)+relation+".\r\n")

@given("player")
def inventory(a):
  say("You have "+ call("list_contents", a, a) + ".\r\n")

@given("player", a("located"))
def drop(a, b):
  if call("move", b, location(a)):
    say("you drop the ", name(b)+".\r\n")
    report_to(location(a), call("indefinate_name", a), "drops the", name(b)+".\r\n")

@given("player", a("located"), a("closed", "container"))
def drop(a, b, c):
  if call("open", a, c):
    return True
  say("You're not able to open it.")
  return False

@given("player", a("located"), "container")
def drop(a, b, c):
  p = path(c)
  print "PATH", map(name, map(from_uid, p))
  if b["uuid"] in p or b["id"] in p:
    say("you can't put something inside of itself.")
    return False
  if call("move", b, c):
    relation = call("scope_relation", c, a)
    say("you put the ", name(b)+" into "+call("indefinate_name", c)+relation+".\r\n")
    report_to(location(a), call("indefinate_name", a), "puts the ", name(b)+" into "+call("indefinate_name", c)+relation+".\r\n")




