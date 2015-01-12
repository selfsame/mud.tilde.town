from mud.core import *
import random
from mud.core.CAPSMODE import *

@construct
def traits(d):
	return {
	"height":random.randint(54,74),
	"haircolor":random.choice(["black","brown","red","blonde"]),
	"age":random.randint(2,112)}

@construct
def gender(d): return random.choice(["m","f"])

_gt = {"m":"man","f":"woman"}

def _male(e): return GET(e,"gender") == "m"
def _female(e): return GET(e,"gender") == "f"

bind.predicate("male", _male)
bind.predicate("female", _female)

@before(has("traits"))
def printed_name(e):
  return e["traits"]["haircolor"]+" haired "

@given(a(has("gender"),has("traits")))
def printed_name(e):
  return str(_gt[e["gender"]])

@given("female")
def plural_name(e): return "women"

@given("male")
def plural_name(e): return "men"