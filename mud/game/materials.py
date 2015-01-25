from mud.core import *

bind.predicate("materialistic", has("material"))
bind.predicate("fabricated", a(has("material"), has("fabricated")))

@construct
def material(d):
  if isinstance(d, dict):
    choice = parse.table_choice(d)
    if choice:
      return choice
    return "stone"
  return d

bind.predicate("stone", key_is("material", "stone"), True)
bind.predicate("flesh", key_is("material", "flesh"), True)
bind.predicate("wood", key_is("material", "wood"), True)
bind.predicate("copper", key_is("material", "copper"), True)
bind.predicate("bronze", key_is("material", "bronze"), True)
bind.predicate("gold", key_is("material", "gold"), True)
bind.predicate("silver", key_is("material", "silver"), True)
bind.predicate("iron", key_is("material", "iron"), True)
bind.predicate("steel", key_is("material", "steel"), True)
bind.predicate("cloth", key_is("material", "cloth"), True)
bind.predicate("leather", key_is("material", "leather"), True)

@given("fabricated")
def adjectives(e):
  return e["material"]


@before(a("copper", "thing"))
def printed_name(e):
  return "{#yellow}"

@before(a("gold", "thing"))
def printed_name(e):
  return "{#bold}{#yellow}"

@before(a("leather", "thing"))
def printed_name(e):
  return "{#yellow}"

@before(a("wood", "thing"))
def printed_name(e):
  return "{#yellow}"

@after(a("fabricated", "thing"))
def printed_name(e):
  return "{#reset}"