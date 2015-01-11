registry = {}

__all__ = ["construct", "serialize", "deserialize", "merge", "_get", "_construct", "_serialize", "_deserialize", "_merge"]

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

def __merge(s, a, b):
    f = _get(s, "merge")
    if f:
        return f(a, b)
    return b

def _serialize(d):
    res = {}
    for k in d:
        f = _get(k, "serialize")
        if f:
            comp = f(d[k])
        else:
            comp = d[k]
        res[k] = comp
    return res

def _deserialize(d):
    res = {}
    for k in d:
        f = _get(k, "deserialize")
        if f:
            comp = f(d[k])
        else:
            comp = d[k]
        res[k] = comp
    return res

def entity_reduce(accum, next):
    for k in next:
        if k in accum:
            accum[k] = __merge(k,accum[k], next[k])
        else:
            accum[k] = next[k]
    return accum

def _merge(col):
    return reduce(entity_reduce, col, {})


def _construct(d):
    res = {}
    for k in d:
        f = _get(k, "construct")
        if f:
            comp = f(d[k])
        else:
            comp = d[k]
        res[k] = comp
    return res