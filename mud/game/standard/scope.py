from mud.core.util import *
from mud.core.actions import *
from predicates import *




@action
@given('located', 'located')
def scope_relation(a, b):
  res = ''
  ah = from_uid(a['located'])
  bh = from_uid(b['located'])
  if has("room")(ah):
    return " on the floor"
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




@action
@given("player", string)
def scope_while(e, a):
  res = act("check_scope", e) 
  return res

@action
@given("player", equals("look"))
def scope_while(e, a):
  return act("check_scope", e) 

@action
@given("player", equals("walk"))
def scope_while(e, a):
  return the(location(e),"exits").keys()

@action
@given("player", equals("drop"))
def scope_1_while(e, a):
  return act("check_inventory_scope", e) 

@action
@given("player", equals("drop"))
def scope_2_while(a, b):
  loc = location(a)
  return act("check_scope", a, loc)


@action
@given("player", equals("drop"), anything)
def scope_while(e, a, b):
  inv = act("check_inventory_scope", e) 
  loc = location(e)
  res = act("check_scope", e, loc)
  return inv + res

@action
@given("player", equals("take"))
def scope_while(e, a):
  return act("check_scope", e, location(e))

@action
@given("player")
def check_scope(a):
  inv = act("check_inventory_scope", a) 
  loc = location(a)
  res = act("check_scope", a, loc)
  return inv + res

@action
@given("entity", "thing")
def check_scope(a, c):
  return [c]

@action
@given(a("player", "holder"))
def check_inventory_scope(a):
  return contents_of(a)


@action
@given("player", "container")
def check_scope(a, b):
  res = [b]
  for item in contents_of(b):
    f = act("check_scope", a, item)
    if f: 
      res += f
  return res


@action
@given("entity", a("closed", "container"))
def check_scope(a, c):
  return [c]


# @action
# @given("entity", a("hidden", "thing"))
# def check_scope(a, c):
#   return []
