from mud.core import *

@given("player", string)
def input(a, b):
	tokens = verbs.determine(b)
	call("input", a, tokens[0], tokens[1:])

@given("player", verb, sequential)
def input(p, v, tokens):
	scope = call("scope_while", p, v)
	res = map(lambda x: call("resolve", x, scope), tokens)

	if apply(call, ["object_blocked", v, p] + [res]): return False

	#inoke the verb with player and resolved objects
    apply(call, [v, p] + res)

@given("player", verb, "[]")
def input(a, b):
	pass

@given("player", "token", sequential)
def resolve(a, b):
	pass