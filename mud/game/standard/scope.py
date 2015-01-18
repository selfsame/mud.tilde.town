from mud.core.util import *
from mud.core import *

@given('located', 'located')
def scope_relation(a, b):
  res = ''
  ah = from_uid(a['located'])
  bh = from_uid(b['located'])
  if has("room")(ah):
    return ""
  elif has("player")(ah):
    res += " in "+name(ah)+"'s inventory"
  else:
    res += " inside the "+name(ah)+""
  if ah.get("located"):
    ah2 = from_uid(ah['located'])
    if not has("room")(ah2):
      if has("player")(ah2):
        res += " in "+name(ah2)+"'s inventory"
      else:
        res += " in the "+name(ah2)+""
  return res



@given("player", string)
def scope_while(e, a):
  res = call("check_scope", e) 
  return res

@given("player", equals("look"))
def scope_while(e, a):
  return call("check_scope", e) 

@given("player", equals("walk"))
def scope_while(e, a):
  return the(location(e),"exits").keys()

@given("player", equals("drop"))
def scope_1_while(e, a):
  return call("check_inventory_scope", e) 

# @given("player", equals("drop"))
# def scope_2_while(a, b):
#   loc = location(a)
#   return call("check_scope", a, loc)


@given("player", equals("drop"), anything)
def scope_while(e, a, b):
  inv = call("check_inventory_scope", e) 
  loc = location(e)
  res = call("check_scope", e, loc)
  return inv + res

@given("player", equals("take"))
def scope_while(e, a):
  return call("check_scope", e, location(e))

@given("player")
def check_scope(a):
  inv = call("check_inventory_scope", a) or []
  loc = location(a)
  res = call("check_scope", a, loc) or []
  return inv + res

@given("entity", "thing")
def check_scope(a, c):
  return [c]

@given(a("player", "holder"))
def check_inventory_scope(a):
  res = []
  for item in call("get_contents", a):
    res += call("check_scope", a, item)
  return res


@given("player", "container")
def check_scope(a, b):
  res = [b]
  for item in call("get_contents", b):
    f = call("check_scope", a, item)
    if f: 
      res += f
  return res


@given("entity", a("closed", "container"))
def check_scope(a, c):
  return [c]


# @given("entity", a("hidden", "thing"))
# def check_scope(a, c):
#   return []
