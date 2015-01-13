from mud.core import *
from mud.core.CAPSMODE import *
import re

bind.predicate("token", dictionary)

@given("player", string)
def player_input(a, b):
	data.subject = a
	tokens = verbs.determine(b)
	if not tokens: return False
	if len(tokens) > 0:
		call("player_input", a, GET(tokens,0), tokens[1:])


@given("player", verb, sequential)
def player_input(p, v, tokens):
	scope = call("scope_while", p, v)
	res = map(lambda x: call("resolve_token", p, x, scope), tokens)
	print map(util.name, res)
	if call("object_blocked", v, p, res): return False
	#inoke the verb with player and resolved objects
	apply(call, [v, p] + res)
	#data.subject = False

@given("player", verb, empty)
def player_input(a, b, c):
	call(b, a)

@after("player", anything, anything)
def player_input(a, b, c):
	data.subject = False



@given("player", has("text"), sequential)
def resolve_token(p, token, scope):
	return token["text"]

@given("player", has("noun"), sequential)
def resolve_token(p, token, scope):
	return call("resolve_token", p, token["noun"], scope)

@given("player", has("string"), sequential)
def resolve_token(p, token, scope):
	for item in scope:
		match = call("scope_match", token["string"], item)
		if match: return match

	return token["string"]

@given("player", has("holder"), sequential)
def resolve_token(p, token, scope):
	matches = find_held_scope(token, scope)
	print matches
	if matches: return matches[0]
	return token["string"]


@given(string, has("id"))
def scope_match(s, e):
	if re.match(e["id"], s): return e
	if re.match( "|".join(str((call("indefinate_name", e))).split(" ")), s):return e

@given(string, has("name"))
def scope_match(s, e):
	if re.match(str(e["name"]), s): return e
	if re.match( "|".join(str((call("indefinate_name", e))).split(" ")), s):return e


@given(string, has("regex"))
def scope_match(s, e):
	if re.match(str(e["regex"]), s): return e
	if re.match( "|".join(str((call("indefinate_name", e))).split(" ")), s):return e


def scope_matches(scope, s):
	res = []
	for item in scope:
		match = call("scope_match", s, item)
		if match: res.append(match)
	return res

def get_holder_stack(cursor, stack=[]):
  stack = [cursor] + stack
  if "holder" in cursor:
    return get_holder_stack(cursor["holder"], stack)
  else:
    return stack

def find_held_scope(cursor, scope):
  stack = get_holder_stack(cursor["holder"])
  if stack:
    scopes = [scope]
    for item in stack:
      paths = []
      for branch in scopes:
        hs = filter(bound("container"), branch)
        matches = scope_matches(hs, item["string"])
        if matches:
          for m in matches:
            paths.append(contents_of(m))
      scopes = paths
    res = []
    for branch in scopes:
      res += scope_matches(branch, cursor["string"])
    return res