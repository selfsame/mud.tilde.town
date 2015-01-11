from mud.core import *

@construct
def contents(d):
  res = []
  for e in d:
    if e.get("id"):
      c_e = components._construct(e)
      new = data.instance(e.get("id"), False)
      merged = components._merge([new, c_e])
      data.register(merged)
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
  if "contents" in e:
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



@given("container")
def get_contents(p, r):
  es = r["contents"]
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

@before(a("closed", "container"))
def printed_name(e):
  return "closed "

@before(a("open", "container"))
def printed_name(e):
  return "open "

@after(a("open", "container"))
def indefinate_name(e):
  return " (containing "+call("list_contents", e)+")"

@after(a("open", "empty", "container"))
def indefinate_name(e):
  return "(empty)"


@given("player", a("open", "container"))
def open(a, b):
  say("It's allready opened.")

@given("player", a("closed", "container"))
def close(a, b):
  say("It's allready closed.")

@given("player", a("closed", "container"))
def open(a, b):
  b["closed"] = False
  relation = call("scope_relation", b, a)
  say("You open the "+name(b)+relation+".")
  report_to(location(a), call("indefinate_name", a), "opens the ", name(b)+relation+".")
  return True

@given("player", a("open", "container"))
def close(a, b):
  b["closed"] = True
  relation = call("scope_relation", b, a)
  say("You close the "+name(b)+relation+".")
  report_to(location(a), call("indefinate_name", a), "closes the ", name(b)+relation+".")
  return True