from mud.core.actions import *
from mud.core.util import *
from mud.core import predicates
from mud.core.predicates import *
from mud.core.components import *
from mud.core.components import _serialize, _merge, _construct

predicates.register("holder", has('contents'))
predicates.register("container", a(non("entity"), "holder"))

def empty(e):
  if "contents" in e:
    c = len(e["contents"])
    if c == 0: return True
  return False

predicates.register("empty", empty)

def closed(e):
  if has("closed")(e):
    if e["closed"] == True:
      return True
  return False

predicates.register("closed", closed)
predicates.register("open", non("closed"))


@construct
def contents(d):
  res = []
  for e in d:
    if e.get("id"):
      c_e = _construct(e)
      new = instance(e.get("id"))
      merged = _merge([new, c_e])
      register(merged)
      res.append(merged.get("uuid"))
  return res

@serialize
def contents(d):
  conts = map(from_uid, d)
  return map(_serialize, conts)





@action
@given("container")
def get_contents(p, r):
  es = r["contents"]
  res = []
  for s in es:
    er = data.instances.get(s)
    if er: res.append(er)
  return res

@after
@given("player", a("open", "container"))
def look(p, r):
  say("Inside it you see "+ act("list_contents", p, r)+ ".")

@after
@given("player", a("empty", "container"))
def look(p, r):
  say("It's completely empty.")

@before
@given(a("closed", "container"))
def printed_name(e):
  return "closed "

@before
@given(a("open", "container"))
def printed_name(e):
  return "open "

@after
@given(a("open", "container"))
def indefinate_name(e):
  return " (containing "+act("list_contents", e)+")"

@after
@given(a("open", "empty", "container"))
def indefinate_name(e):
  return "(empty)"


@action
@given("player", a("open", "container"))
def open(a, b):
  say("It's allready opened.")

@action
@given("player", a("closed", "container"))
def close(a, b):
  say("It's allready closed.")

@action
@given("player", a("closed", "container"))
def open(a, b):
  b["closed"] = False
  relation = act("scope_relation", b, a)
  say("You open the "+name(b)+relation+".")
  report_to(location(a), act("indefinate_name", a), "opens the ", name(b)+relation+".")
  return True

@action
@given("player", a("open", "container"))
def close(a, b):
  b["closed"] = True
  relation = act("scope_relation", b, a)
  say("You close the "+name(b)+relation+".")
  report_to(location(a), act("indefinate_name", a), "closes the ", name(b)+relation+".")
  return True