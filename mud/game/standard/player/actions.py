from mud.core import *
from colors import color
from mud.core.util import *
from mud.core.CAPSMODE import *


bind.verb("talk", "say|[\']", {"past":"said"})
bind.verb_pattern("talk", "{1:text}")

bind.verb("tell", "tell", {"past":"told"})
bind.verb_pattern("tell", "{1} [\'\"]*{2:text}[\'\"\?]*")

bind.verb("ask", "ask", {"past":"asked"})
bind.verb_pattern("ask", "{1:text}","{1} [\'\"]*{2:text}[\'\"\?]*")

@given("entity", string)
def talk(a, b):
  if b.strip()[-1] == "?":
    understood.objects([b.strip()[:-1]])
    call("ask", a, b)
    understood.previous()
    return True
  understood.subject(a)
  report("[Subject] say[s] '{#bold}{#yellow}[object]{#reset}'.")
  understood.previous()


@given("entity", "entity", string)
def tell(a, b, c):
  print understood.objects()
  understood.subject(a)
  understood.objects([b, c])
  print understood.objects()
  report("[Subject] says '{#bold}{#yellow}[second object]{#reset}' to [object].")
  understood.previous()
  understood.previous()

@given("entity", "entity", string)
def ask(a, b, c):
  understood.subject(a)
  report("[Subject] ask[s] [object] '{#bold}{#cyan}[second object]{#reset}?'")
  understood.previous()

@given("entity", string)
def ask(a, b):
  understood.subject(a)
  report("[Subject] ask[s] '{#bold}{#cyan}[object]{#reset}?'")
  understood.previous()

@before("player", "player")
def print_name_for(a, b):
  if a != b:
    return "{#magenta}"

@after("player", "player")
def print_name_for(a, b):
  if a != b:
    return "{#reset}"

@after("player", anything)
def walk(a, b):
  call("look", a)





@given("player")
def look(a):
  r = location(a)
  call("describe", a, r)

@given("player", sequential)
def look(a, col):
  print "look(a, col)"
  say(str(call("list_contents", col)))


@given("player", undefined)
def look(a, b):
  say("you dont see anything like that here.")


@given("entity", "thing")
def look(a, b):
  relation = call("scope_relation", b, a) or ""
  report("[Subject] [verb] at [object].")

@given("player", "thing")
def look(a, b):
  relation = call("scope_relation", b, a) or ""
  report("[Subject] [verb] at [object].")
  say(call("write",b,'desc'))

@given("player", anything)
def take(a, b):
  say("That's not something you could take.")

@check("player", sequential)
def take(a, col):
  map(INF(call, "take", a, "%1"), col)

@check("player", a("fixed", "object"))
def take(a, b):
  say("You try, but it seems to be permamently attached.")
  return False

@check("player", a(non("object"), "entity"))
def take(a, b):
  say("Maybe if it was unconscious, or dead..")
  return False


@given("player", a("located", "object"))
def take(a, b):
  understood.objects([b])
  relation = call("scope_relation", b, a) or ""
  if call("move", b, a):
    report("[Subject] pick[s] up [object]"+relation+".")
  understood.previous()


@given("player")
def inventory(a):
  say("You have "+ call("list_contents", a, a) + ".\r\n")

@given("player", a("located"))
def drop(a, b):
  understood.objects([b])
  if call("move", b, call("get_location",a)):
    report("[Subject] [verb] [object].")
  understood.previous()

@check("player", anything, a("closed", "container"))
def drop(a, b, c):
  if call("open", a, c):
    return True
  say("You're not able to open it.")
  return False


@given("player", sequential)
def drop(a, col):
  map(INF(call, "drop", a, "%1"), col)



@given("player", a("located"), "holder")
def drop(a, b, c):
  understood.objects([b, c])
  if call("move", b, c):
    relation = call("scope_relation", c, a) or ""
    report("[Subject] put[s] [object] into [second object]"+relation+".")
  understood.previous()

@check("player", "thing", "holder")
def drop(a, b, c):
  p = util.path(b)
  if b == c or c["uuid"] in p or c["id"] in p:
    say("you can't put something inside of itself.")
    return False
  return True

@check("player", sequential, "container")
def drop(a, col, c):
  map(INF(call, "drop", a, "%1", c), col)


