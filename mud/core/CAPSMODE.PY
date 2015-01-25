
def GET(col, k, notfound=None):
  try: return col[k]
  except: return notfound

def GET_IN(col, ks, notfound = None):
  for k in ks:
    col = GET(col, k, notfound)
  return col

def KEYFN(k):
  def _KEYFN_(col, nf=None): return GET(col, k, nf)
  return _KEYFN_

def NONE(v): return v is None
def NOT(v): return not v
def FIRST(col): return GET(col, 0)

def COMP(*args):
  def _COMP_(v):
    for f in args:
      if not f(v): return False
    return True
  return _COMP_

def INVERT(*args):
  def _INVERT_(x): 
    for f in args:
      if f(x): return False
    return True
  return _INVERT_

_1 = "%1"
_2 = "%2"
_3 = "%3"
_4 = "%4"
_5 = "%5"

def INF(f, *args):
  def _INF_(*_args): return apply(f, _SWAP(list(args), list(_args)))
  return _INF_

def _SWAP(col, args):
  for idx, v in enumerate(args):
    w = GET([_1, _2, _3, _4, _5], idx)
    if w in col:
      widx = col.index(w)
      col.remove(w)
      col.insert(widx, v)
  return col


def GROUP_BY(f, col):
  res = {}
  for i in col:
    v = f(i)
    if GET(res, v):
      res[v].append(i)
    else:
      res[v] = [i]
  return res

