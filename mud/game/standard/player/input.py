from mud.core import *
from mud.core.CAPSMODE import *
import re

bind.predicate("token", dictionary)

@given("player", string)
def player_input(a, b):
	understood.subject(a)
	print util.name(call("get_location", a))
	print map(util.name, call("get_contents", call("get_location", a)))
	understood.scope(call("get_contents", call("get_location", a)))
	tokens = verbs.determine(b)
	if not tokens: return False
	if len(tokens) > 0:
		call("player_input", a, GET(tokens,0), tokens[1:])


@given("player", verb, sequential)
def player_input(p, v, tokens):
	understood.verb(v)
	scope = call("scope_while", p, v)
	res = []
	for idx, t in enumerate(tokens):
		_scope = False
		_scope = call("scope_"+str(idx+1)+"_while", p, v)
		if not _scope: _scope = scope
		res.append(call("resolve_token", p, t, _scope))
	understood.objects(res)
	print [v] + map(util.name, res)
	if call("object_blocked", v, p, res): return False
	#inoke the verb with player and resolved objects
	apply(call, [v, p] + res)


@given("player", verb, empty)
def player_input(a, b, c):
	call(b, a)

@after("player", anything, anything)
def player_input(a, b, c):
	understood.reset()


def _plural(s):
	words = parse.words(s)
	lastword = words.pop()
	if GET(bind._plural_kinds, lastword): 
		return True
	return False


@given("player", has("text"), sequential)
def resolve_token(p, token, scope):
	return token["text"]

@given("player", has("noun"), sequential)
def resolve_token(p, token, scope):
	return call("resolve_token", p, token["noun"], scope)

@given("player", has("string"), sequential)
def resolve_token(p, token, scope):
	if token["string"] in ["me", "myself"]: 
		return p
	matches = scope_matches(scope, token["string"])
	if _plural(token["string"]): 
		return matches
	return GET(matches, 0, token["string"])

def passes(item, adjs):
	for adj in adjs:
		if not adj(item):
			return False
	return True


@given(string, sequential, sequential)
def resolve_singular_kind(kind, adjs, scope):
	res = []
	for item in scope:
		if kind in GET(item, "kind", []): 
			if passes(item, adjs):
				res.append(item)
	return res

@given(string, sequential, sequential)
def resolve_plural_kind(kind, adjs, scope):
	res = []
	for item in scope:
		if kind in GET(item, "kind", []): 
			if passes(item, adjs):
				res.append(item)
	return res

@given("player", has("holder"), sequential)
def resolve_token(p, token, scope):
	matches = find_held_scope(token, scope)
	if matches: return matches[0]
	return token["string"]


@given(string, has("id"))
def scope_match(s, e):
	if re.match(e["id"], s): return e
	if re.match( "^"+"$|^".join(str(parse.plain(call("print_name_for", e, understood.subject()))).lower().split(" "))+"$", s):return e

@given(string, has("name"))
def scope_match(s, e):
	if re.match(str(e["name"]), s): return e
	if re.match( "^"+"$|^".join(str(parse.plain(call("print_name_for", e, understood.subject()))).lower().split(" "))+"$", s):return e


@given(string, has("regex"))
def scope_match(s, e):
	if re.match(str(e["regex"]), s): return e
	if re.match( "^"+"$|^".join(str(parse.plain(call("print_name_for", e, understood.subject()))).lower().split(" "))+"$", s):return e


def scope_matches(scope, s):
	words = parse.words(s)
	lastword = words.pop()
	adjs = []
	for w in words:	
		if GET(bind._adjectives, w): 
			pred = bound(GET(bind._adjectives, w))
			if pred:
				adjs.append(pred)

	if GET(bind._plural_kinds, lastword): 
		print "PLURAL"
		match = call("resolve_plural_kind", GET(bind._plural_kinds, lastword), adjs, scope)
		if match: return match
	elif GET(bind._singular_kinds, lastword):
		print "SINGULAR"
		match = call("resolve_singular_kind", GET(bind._singular_kinds, lastword), adjs, scope)
		if match:  return match

	res = []
	for item in scope:
		match = call("scope_match", lastword, item)
		if match: 
			if passes(match, adjs):
				res.append(match)
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
            paths.append(call("get_contents", m))
      scopes = paths
    res = []
    print "find_held_scope:",cursor["string"]

    for branch in scopes:
      bmatches = scope_matches(branch, cursor["string"])
      res += bmatches
    print cursor["string"]
    if _plural(cursor["string"]): return [res]
    return res