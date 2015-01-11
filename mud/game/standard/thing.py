from mud.core import *

bind.predicate("thing", dictionary)
bind.predicate("registered", has("uuid"))
bind.predicate("object", has("object"))

def _datatype(s): 
	if string(s):
		if s in data.datatypes: return True
		return False

bind.predicate("datatype", _datatype)


@merge
def kind(p=[], n=[]):
  return list(set(p + n))
