from util import from_uid, contents_of, name
from predicates import has
from parse import template
from mud.core.dispatch import call
from CAPSMODE import *
import re

class Context:
	def __init__(self):
		self.reset()

	def last(self, thing, nf=None):
		return GET(thing, len(thing)-1, nf)

	def _handle(self, prop, v=None, nf=None):
		if v:
			prop.append(v)
			self._stack.append(prop)
		else:
			return self.last(prop, nf)

	def subject(self, v=None):
		return self._handle(self._subject, v, {})

	def scope(self, v=None):
		return self._handle(self._scope, v, [])

	def verb(self, v=None):
		return self._handle(self._verb, v)

	def objects(self, v=None):
		return self._handle(self._objects, v, [])

	def previous(self):
		try: self._stack.pop().pop()
		except: pass

	def reset(self):
		self._stack = []
		self._subject = []
		self._verb = []
		self._objects = []
		self._scope = []


understood = Context()


def _resolve(code, observer):
	print "_resolve",code
	if code == "": return ""
	code = code[1:-1].strip()
	if len(code) == 0: return ""
	capital = False
	if code[0] == code[0].upper(): capital = True
	code = code.lower()
	res = ""
	if code == "subject":
		res = call("print_for", understood.subject(), observer)
	elif code in ["itself","himself","theirself","herself","theirselves"]:
		res = call("print_object_for", understood.subject(), observer)
	elif code == "object":
		res = call("print_object_for", GET(understood.objects(), 0), observer)
	elif code == "second object":
		res = call("print_object_for", GET(understood.objects(), 1), observer)
	elif code == "third object":
		res = call("print_object_for", GET(understood.objects(), 2), observer)
	elif code == "fourth object":
		res = call("print_object_for", GET(understood.objects(), 3), observer)
	elif code == "s":
		if understood.subject() == observer: res = ""
		else: res = "s"
	elif code == "verb":
		if understood.subject() == observer:
			res = understood.verb()
		else: res = understood.verb() + "s"
	res = str(res)
	if capital: res = res[0].upper()+res[1:]
	return res

def _separate(pattern, s):
  rs = re.findall(pattern, s) + [""]
  res = re.split(pattern, s)
  return (rs, res)

def _contextualize(s, observer):
  unzip = _separate('\[[^\[\]]*\]', s)
  swap = map(INF(_resolve, "%1", observer), unzip[0])
  zipped = [val for pair in zip(unzip[1], swap) for val in pair]
  print zipped
  return "".join(zipped)

def say(*args):
  player = understood.subject()
  if GET(player, "player"):
    player['player'].sendLine(template("".join(args)))

def report(*args):
  observers = filter(has("player"), understood.scope())
  for actor in observers:
    actor["player"].sendLine(template(_contextualize(" ".join(args), actor)))

def report_to(room, *args):
  observers = map(from_uid, contents_of(room))
  for actor in observers:
    if GET(actor, "player"):
      if understood.subject() != actor:
        actor["player"].sendLine(template(" ".join(args)))