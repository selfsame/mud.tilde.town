import construct as _c
import serialize as _s
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


def construct(d):
    res = {}
    for k in d:
        comp = _construct(k, d[k])
        res[k] = comp
    return res


def serialize(d):
	res = {}
	try:
		for k in d:
			comp = _serialize(k, d[k])
			res[k] = comp
	except:
		print "ERROR SERIALIZING:", d
	return res


