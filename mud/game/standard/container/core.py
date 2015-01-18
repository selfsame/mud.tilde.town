from mud.core import *
from mud.core.util import *

@construct
def contents(d):
  res = []
  for e in d:
    if e.get("id"):
      c_e = components._construct(e)
      new = data.instance(e.get("id"), False)
      merged = components._merge([new, c_e])
      data.register(merged)
      dispatch.stack("init", merged)
      res.append(merged.get("uuid"))
  return res

@merge
def contents(a, b):
  return a + b

@serialize
def contents(d):
  conts = map(util.from_uid, d)
  return map(components._serialize, conts)

bind.predicate("holder", has('contents'))
bind.predicate("container", a(non("entity"), "holder"))

def empty(e):
  if has("contents")(e):
    c = len(e["contents"])
    if c == 0: return True
  return False

bind.predicate("empty", empty)

def closed(e):
  if has("closed")(e):
    if e["closed"] == True:
      return True
  return False

bind.predicate("closed", closed)
bind.predicate("open", a(has("closed"), non("closed")))

bind.adjective("closed", "closed")
bind.adjective("open", "open")


@given("holder")
def get_contents(c):
  es = c["contents"]
  res = []
  for s in es:
    er = data.instances.get(s)
    if er: res.append(er)
  return res

@after("player", a("open", "container"))
def look(p, r):
  say("Inside it you see "+ call("list_contents", p, r)+ ".")

@after("player", a("empty", "container"))
def look(p, r):
  say("It's completely empty.")

@given(a("closed", "container"))
def adjectives(e):
  return "closed"

@given(a("open", "container"))
def adjectives(e):
  return "open"

# @after(a("open", "container"))
# def printed_name(e):
#   return " (containing "+call("list_contents", call("get_contents", e))+")"

@before(a("open", "empty", "container"))
def adjectives(e):
  return "empty"




@given("player", a("open", "container"))
def open(a, b):
  say("It's allready opened.")

@given("player", a("closed", "container"))
def close(a, b):
  say("It's allready closed.")

@given("player", a("closed", "container"))
def open(a, b):
  understood.objects([b])
  relation = str(call("scope_relation", b, a))
  report("[Subject] open[s] [object]"+relation+".")
  b["closed"] = False
  understood.previous()
  return True

@given("player", a("open", "container"))
def close(a, b):
  understood.objects([b])
  relation = str(call("scope_relation", b, a))
  report("[Subject] close[s] [object]"+relation+".")
  b["closed"] = True
  understood.previous()
  return True