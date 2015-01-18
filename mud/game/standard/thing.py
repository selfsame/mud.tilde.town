from mud.core import *
import copy

bind.predicate("thing", dictionary)
bind.predicate("registered", has("uuid"))
bind.predicate("object", has("object"))


def _datatype(s): 
	if string(s):
		if s in data.datatypes: return True
		return False

bind.predicate("datatype", _datatype)

@construct
def kind(d):
	for k in d:
		bind.kind(k)
	return copy.copy(d)

@merge
def kind(p=[], n=[]):
  return list(set(p + n))

