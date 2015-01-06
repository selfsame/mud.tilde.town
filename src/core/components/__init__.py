import construct as _c
import serialize as _s
import merge as _m
import core
from core import make, instance, load, register, delete


def _construct(s, d):
    f = _c._symbol(s)
    if f:
        return f(d)
    return d

def _serialize(s, d):
    f = _s._symbol(s)
    if f:
        return f(d)
    return d

def _merge(s, a, b):
    f = _m._symbol(s)
    if f:
        return f(a, b)
    return b


def construct(d):
    res = {}
    for k in d:
        comp = _construct(k, d[k])
        res[k] = comp
    return res


def serialize(d):
	res = {}
	for k in d:
		comp = _serialize(k, d[k])
		res[k] = comp
	return res

def entity_reduce(accum, next):
    for k in next:
        if k in accum:
            accum[k] = _merge(k,accum[k], next[k])
        else:
            accum[k] = next[k]
    return accum

def merge(col):
    return reduce(entity_reduce, col, {})


