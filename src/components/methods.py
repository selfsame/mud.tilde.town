import data


def has(thing, compstr, default=False):
    if compstr in thing:
        return thing[compstr]
    else:
        return default

def name(thing):
  return has(thing, "name", has(thing, "firstname", has(thing, "ustr", "thing")))

def plural_name(thing):
  return has(thing, "plural", name(thing) + "s")

def description(thing):
  return has(thing, "description", has(thing, "desc", "There is nothing unusual about it."))

def get_room(s):
  if isinstance(s, str):
    r = data.rooms.get(s)
    if r:
      return r
  elif isinstance(s, dict):
    if s.get('room'):
      return s

def send_room(r, s):
  room = get_room(r)
  contents = has(room['room'], "contents", [])
  for e in contents:
    i = data.instances.get(e)
    if i and has(i,"player"):
      i["player"].con.sendLine(s)


