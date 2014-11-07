from methods import *
import construct as _c
import serialize as _s
import update as _u
import make as _make
from make import instance, load

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
        f(d, delta)

def test():
    load("edit")
    whale = instance("whale")
    mouse = instance("mouse")
    print whale
    print mouse
