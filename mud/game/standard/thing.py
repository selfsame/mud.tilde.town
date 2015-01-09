from mud.core import *

predicates.register("thing", predicates.dictionary)
predicates.register("registered", predicates.has("uuid"))
predicates.register("object", predicates.has("object"))

def _datatype(s): 
	if predicates.string(s):
		if s in data.datatypes: return True
		return False

predicates.register("datatype", _datatype)

@construct
def extends(d):
  return map(instance, d)

@merge
def kind(p=[], n=[]):
  return list(set(p + n))



# @action
# @given("datatype")
# def _instance(s):
#   pass

# @action
# @given("thing")
# def register(s):
#   pass

# @action
# @given("thing")
# def delete(s):
#   pass