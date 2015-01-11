from mud.core import verbs, predicates

__all__ = ['predicate','verb']


def predicate(s, f): return predicates._register(s, f)

def verb(name, regex, tenses = {}): return verbs.register(name, regex, tenses)

def verb_pattern(v, *patterns): return apply(verbs.register_structure, [v] + list(patterns))