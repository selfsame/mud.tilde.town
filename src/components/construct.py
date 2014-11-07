import make

"""
component constructor functions.  
1 arg: datatype component value, return the instanced component value.

"""

def _symbol(s):
  try:
    return globals()[s]
  except:
    return False

def extends(d):
    res = {}
    for ustr in d:
        res = dict(res.items() + make.instance(ustr).items())
    return res

def living(d):
    d['hp'] = d['hpmax']
    return d

