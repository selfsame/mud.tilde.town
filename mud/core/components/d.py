registry = {}

__all__ = ["construct", "serialize", "deserialize", "merge", "_get"]

def tunnel(cursor, key, notfound={}):
  if key not in cursor:
    cursor[key] = notfound
  return cursor[key]

def walk(cursor, key):
  if cursor:
    if cursor.get(key):
      return cursor[key]
  return False


def _register(f, tag):
    v = f.__name__
    cursor = tunnel(registry, v, {})
    cursor = tunnel(cursor, tag, f)    

def construct(f):
  _register(f, "construct")  
  return f

def serialize(f):
  _register(f, "serialize")  
  return f

def deserialize(f):
  _register(f, "deserialize")  
  return f

def merge(f):
  _register(f, "merge")  
  return f


def _get(k, s):
    if k in registry:
        if s in registry[k]:
            return registry[k][s]
