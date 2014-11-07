


def has(thing, compstr, default=False):
    if compstr in thing:
        return thing[compstr]
    else:
        return default

def name(thing):
  return has(thing, "name", has(thing, "ustr", "thing"))

def plural_name(thing):
  return has(thing, "plural", name(thing) + "s")

def description(thing):
  return has(thing, "description", "There is nothing unusual about it.")
