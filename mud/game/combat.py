from mud.core import *
import random

bind.verb("kill", "kill|k|attack", {"doc":"Initiates combat with an opponent."})
bind.verb_pattern("kill", "{1}")

@check("player", non("entity"))
def kill(a, b):
  say("You can't attack "+str(call("print_for", b, a))+".")
  return False

@check("player", undefined)
def kill(a, b):
  return False

@check("entity", "entity")
def kill(a, b):
  if a == b: 
    say("You can't attack yourself.")
    return False
  return True

@given("entity", "entity")
def kill(a, b):
  call("strike", a, b)
  call("strike", b, a)
  if random.randint(0,10) < 2:
    report("[Subject] miss[es] [object]!")
  else:
    dam = call("roll_attack", a)
    call("damage", b, dam, a)


@given("entity", "entity")
def strike(a, b):
    if not data.related(b, "attacking", a):
        data.associate("attacking", b, a)
        report("[Subject] begin[s] fighting [object]!")
    else:
        if b["target"] != a["uuid"]:
            report("[Object] start[s] attacking [subject]!")
    b["target"] = a["uuid"]

@check(a("idle", "entity"), number)
def update(a, delta):
    target = GET(data.instances, GET(a, "target"))
    if target:
        conts = call("get_contents", call("get_location", a))
        if conts:
            if target in conts:
                call("enact", a, "kill", target)
            else:
                a["target"] = False
            a['acting']['ap'] = 10
    else:
        return True


@construct
def damage(d):
    return parse.Dice(d)


@serialize
def damage(d):
    return str(d)

@deserialize
def damage(d):
    return parse.Dice(d)



@given(has("living"), number, anything)
def damage(a, b, c):
    #dodge check
    return True

@given("entity", number, "entity")
def damage(a, dam, c):
  report("{#red}[Subject] attack[s] [object] for "+str(dam)+"!{#reset}")
  a["living"]["hp"] -= dam
  if a["living"]["hp"] <= 0:
    exp = GET(a, "expvalue", 0)
    call("die", a)
    c["exp"] += exp
    understood.subject(c)
    say("You gain {0} experience for the kill.".format(exp))
    understood.previous()

@after("player", number, anything)
def damage(a, b, c):
    understood.subject(a)
    say(str(call("line_prompt", a)))
    understood.previous()

@given("entity")
def roll_attack(e):
  dam = GET(e, "damage")
  weap = GET(data.instances, GET(GET(e, "equipment"), "weapon"))
  weapdam = GET(weap, "damage")
  dam = weapdam or dam
  if dam: return dam.roll()
  return 0


@given("entity")
def die(e):
    call("delete", e)

@given("player")
def die(e):
    call("move", e, data.game["rooms"]["afterlife"])
    understood.subject(e)
    say("You shrug off this mortal coil.")
    call("enact", e, "broadcast", "{#magenta}"+e["firstname"]+" has died!{#reset}")
    understood.previous()

@after("entity")
def die(e):
    sc = understood.scope()
    if e in sc: sc.remove(e)
    report("[object] is killed!")


@before(a("located", "entity"))
def die(e):
    loc = call("get_location", e)
    if not loc: return False
    inv = GET(e, "contents", [])
    eq = filter(string, GET(e, "equipment", {}).values())
    res = inv + eq
    for uuid in res:
        if string(uuid):
            print uuid
            item = GET(data.instances, uuid)
            if dictionary(item):
                item["located"] = loc["id"]
                loc["contents"].append(uuid)
    understood.subject(e)
    if res: report("[Subject] drop[s] "+str(call("list_contents", res))+".")
    understood.previous()

@before(a("located", "player"))
def die(e):
    loc = call("get_location", e)
    weap = e["equipment"]["weapon"]
    if weap:
        loc["contents"].append(weap)
        util.from_uid(weap)["located"] = loc["id"]
        e["equipment"]["weapon"] = False
        understood.subject(e)
        understood.objects([util.from_uid(weap)])
        report("[Subject] drop[s] [object].")
        understood.previous().previous()