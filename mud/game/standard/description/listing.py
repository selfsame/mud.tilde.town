from mud.core import *
from util import *

scenic = a("scenic")
bind.predicate("unlisted", has("unlisted"))

@given("player", "holder")
def list_contents(a, b):
  conts = the(b, 'contents')
  #if the(a, 'uuid') in conts: conts.remove(the(a, 'uuid'))
  names = {}
  kinds = {}
  for item in map(from_uid, conts):
    if item == a: break
    if not scenic(item):
      n = call("print_name_for", item, a)
      if names.get(n):
        names[n]  += 1
      else:
        names[n] = 1
      if not kinds.get(n):
        kinds[n] = from_uid(item)
  res = []
  for k in names:
    if names[k] > 1:
      r = "".join(call("indefinate_name", names[k], kinds[k]))
    else:
      r = "".join(act_stack("print_name_for", kinds[k], a))
    if r: res.append( str(r) )
  if len(res) == 0:
    res = ["nothing"]
  lastpair = res[-2:]
  prev = res[:-2] + [" and ".join(lastpair)]
  return ", ".join(prev)

@given(sequential)
def list_contents(b):
  conts = b
  names = {}
  kinds = {}
  for item in conts:
    ent = from_uid(item)
    n = call("print_name_for", ent, understood.subject())
    if names.get(n):
      names[n] += 1
    else:
      names[n] = 1
    if not kinds.get(n):
      kinds[n] = from_uid(item)
  res = []
  for k in names:
    if names[k] > 1:
      r = "".join(call("indefinate_name", names[k], kinds[k]))
    else:
      r = "".join(act_stack("print_name_for", kinds[k], understood.subject()))
    if r: res.append( str(r) )
  lastpair = res[-2:]
  prev = res[:-2] + [" and ".join(lastpair)]
  return  ", ".join(prev)
  


@given("holder")
def list_contents(b): 
  print "list_contents(holder)"
  return act("list_contents", b['contents'])


@given("player", sequential)
def smart_list(a, b):
  conts = b
  known = []
  kinds = {}
  for item in conts:
    if data.related(a, "knows", b):
      known.append(item)
    else:
      typekinds = GET(item, "kind")
      for tk in typekinds:
        kinds[tk] = GET(kinds, tk, []).append(item)









