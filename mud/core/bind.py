from mud.core import verbs, predicates

__all__ = ['predicate','verb', 'kind']

_kinds = {}
_singular_kinds = {}
_plural_kinds = {}
_adjectives = {}

def predicate(s, f): return predicates._register(s, f)

def verb(name, regex, tenses = {}): return verbs.register(name, regex, tenses)

def verb_pattern(v, *patterns): return apply(verbs.register_structure, [v] + list(patterns))

def kind(s):
	sp = s.split("|")
	if len(sp) != 2: return
	if s not in _kinds:
		_kinds[s] = True
		_singular_kinds[sp[0]] = s
		_plural_kinds[sp[1]] = s

def adjective(s, predicate):
	if s not in _adjectives:
		_adjectives[s] = predicate