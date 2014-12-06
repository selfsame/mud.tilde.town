from methods import *
import construct as _c
import serialize as _s
import update as _u
import actions as _a
import make as _make
from make import instance, load, register

def construct(s, d):
    f = _c._symbol(s)
    if f:
        return f(d)
    return d

def serialize(s, d):
    f = _s._symbol(s)
    if f:
        return f(d)
    return {}

def update(s, d, delta):
    f = _u._symbol(s)
    if f:
        return f(d, delta)

def action(a, k, e, arg1):
    f = _a._symbol(a+"_"+k)
    if f:
      return f(e, arg1)

def act(v, e, arg1):
  for k in e:
    f =  action(v, k, e, arg1)

