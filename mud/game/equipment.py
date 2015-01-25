from mud.core import *
from mud.core.CAPSMODE import *

@merge
def equipment(a, b):
  if not isinstance(a, dict): return b
  res = {}
  for slot in a:
    res[slot] = GET(b, slot,  GET(a, slot, False))
  return res

@construct
def equipment(a):
  if not isinstance(a, dict): return {}
  res = {}
  for slot in a:
    if isinstance(a[slot], dict):
      choice = parse.table_choice(a[slot])
      if choice:
        if choice is "False":
          res[slot] = False
        else:
          new = data.instance(choice)
          res[slot] = GET(new, "uuid")
    else: 
      res[slot] = a[slot]
  return res

@serialize
def equipment(d):
  for slot in d:
    uuid = d[slot]
    if isinstance(uuid, str):
      item = util.from_uid(uuid)
      if item:
        d[slot] = components._serialize(item)
  return d

@deserialize
def equipment(d):
  for slot in d:
    item = d[slot]
    if isinstance(item, dict):
      item = components._deserialize(item)
      data.register(item)
      d[slot] = item["uuid"]
  return d


bind.predicate("wearable", has("equippable"), True)

bind.verb("equipment", "eq|gear", {"doc":"Shows what you have equiped.."})
bind.verb_pattern("equipment", "{1}")

bind.verb("wear", "wear", {"doc":"Equips a piece of equipment."})
bind.verb_pattern("wear", "{1} {2}")

bind.verb("remove", "remove", {"doc":"Removes a piece of equipment or readied weapon."})
bind.verb_pattern("remove", "{1}")

bind.verb("wield", "wield",{"doc":"Readies a weapon."})
bind.verb_pattern("wield", "{1} {2}")

@check("player")
def equipment(a):
  say("\r\n")
  weapon = GET(data.instances, a["equipment"]["weapon"])
  if weapon:
    say("{#bold}{#cyan}wielded{#reset}: "+str(call("print_for", weapon, a))    +"({#magenta}"+str(GET(weapon, "damage"))+"{#reset}).")
  for slot in a["equipment"]:
    if slot != "weapon":
      item = GET(data.instances, a["equipment"][slot], False)
      if item: 
        item = str(call("print_for", item, a))     
        say("{#reset}{#bold}{#yellow}"+str(slot)+": {#reset}{#reset}"+str(item)+"{#reset}.")
  say("\r\n")

@check("player", non("wearable"))
def wear(a, b):
  say("That's not something you could wear.")
  return False

@given("player", "wearable")
def wear(a, b):
  equip = a["equipment"]
  slot = GET(b, "slot")
  worn = GET(data.instances, GET(equip, slot))
  if worn:
    understood.objects([worn])
    report("[Subject] remove[s] [object] from "+str(slot)+".")
    understood.previous()
    a["contents"].append(worn["uuid"])
    worn["located"] = a["uuid"]
  if call("unlocate", b):
    report("[Subject] wear[s] [object].")
    equip[slot] = b["uuid"]

@given("player", has("weapon"))
def wield(a, b):
  equip = a["equipment"]
  worn = GET(data.instances, GET(equip, "weapon"))
  if worn:
    understood.objects([worn])
    report("[Subject] stops wielding [object].")
    understood.previous()
    a["contents"].append(worn["uuid"])
    worn["located"] = a["uuid"]
  if call("unlocate", b):
    report("[Subject] wield[s] [object].")
    equip["weapon"] = b["uuid"]

@check("player", "wearable")
def remove(a, b):
  if a["equipment"][b["slot"]] != b["uuid"]:
    say("You're not wearing that.")
  return True

@given("player", "wearable")
def remove(a, b):
  equip = a["equipment"]
  slot = GET(b, "slot")
  report("[Subject] remove[s] equipment from "+str(slot)+".")
  a["contents"].append(b["uuid"])
  b["located"] = a["uuid"]
  a["equipment"][slot] = False






@given(a("player", "holder", has("equipment")))
def check_inventory_scope(a):
  res = []
  for item in call("get_contents", a):
    res += call("check_scope", a, item)
  res += call("equipment_scope", a)
  return res

@given(has("equipment"))
def equipment_scope(a):
  res = []
  for slot in a["equipment"]:
    item = a["equipment"][slot]
    if item: item = GET(data.instances, item)
    if item: res.append(item)
  return res

@given("player", equals("remove"))
def scope_while(e, a):
  return call("equipment_scope", e)


def _armed(e):
  weap = GET(GET(e, "equipment"), "weapon")
  if weap:
    if GET(data.instances, GET(weap, "uuid")):
      return True
    return True
  return False

bind.predicate("armed", _armed)
bind.predicate("unarmed", non("armed"))

bind.adjective("armed", "armed")
bind.adjective("unarmed", "unarmed")

@after("player", has("equipment"))
def look(a, b):
  weapon = GET(data.instances, b["equipment"]["weapon"])
  if weapon:
    say("{#cyan}They wield "+str(call("list_contents", [weapon]))+".{#reset}")

  res = []
  for slot in b["equipment"]:
    if slot != "weapon":
      item = GET(data.instances, b["equipment"][slot], False)
      if item: res.append(item)
  if res:
    desc = call("list_contents", res)
    if desc:
      say("{#yellow}They are wearing "+desc+".{#reset}\r\n")


bind.verb("stats", "stats")

@merge
def stats(a, b):
  res = {}
  for stat in a:
    nex = GET(b, stat, a[stat])
    res[stat] = nex
  return res

@given(has("equipment"))
def get_AC(b):
  ac = 0
  for slot in b["equipment"]:
    item = GET(data.instances, b["equipment"][slot], False)
    ac += GET(item, "AC", 0)
  return ac



@given(a("player", has("equipment"), has("stats")))
def stats(a):
  say("\r\nLEVEL:  "+str(GET(a, "level", 0)))
  say("EXP:  "+str(GET(a, "exp", 0)))
  say("AC:  "+str(call("get_AC", a)))
  say("--------------------")
  for pair in a["stats"].items():
    say("{#green}"+str(pair[0])+"{#reset}:{#yellow}{#bold}"+str(pair[1])+"{#reset}")
  say("\r\n")

@given(a(has("stats"), has("statmod")))
def init(e):
  for stat in e["stats"]:
    e["stats"][stat] += GET(e["statmod"], stat, 0)
  del e["statmod"]