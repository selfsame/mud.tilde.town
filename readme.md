mud.tilde.town
==============

***A python MUD for interactive fiction***

![](http://www.selfsamegames.com/screens/ttmud.png)



#Features

## extensive function dispatching
* inspired by inform7
* functions dispatch for argument arity, argument predicate, and lifecycle variations (check, before, during, after)
* Rich behavior trees are easily created by covering basic functionality then narrowing down edge cases to augment/ovveride.
* functions and predicates are declarativly registered, avoiding import dependencies between game modules

```python
@action
@given("entity", a("closed", "container"))
def close(a, b):
  say("It's already closed.")

@action
@given("entity", a("opened", "container"))
def close(a, b):
  b["closed"] = True
  say("You close "+act("indefinate_name", b)+".")
```

## component/entity game objects:
* data based definitions, .json files or python dicts.
* components are the key value pairs.
* Constructing/serializing/merging functions easily declared for components.
* Can extend by mergine from multiple ancestors.
* Directory structure of entity .json can declare inheritance via ```_base_.json``` files


```json
{"id":"chest",
"name":"wooden chest",
"descripton":"It is likely to have a thing or two inside",
  "extends":["object"],
  "contents":[{"id":"mouse"}],
  "capacity":5,
  "closed":true,
  "opaque":true}
```

```python
from mud.core import *

#component lifecycles

@construct
def contents(d):
	return map(the("uuid"), map(instance, d))

@serialize
def contents(d):
  return map(_serialize, map(util.from_uid, d))

#predicate declaration

predicates.register("container", has('contents'))

def empty(e): return len(the("contents")) == 0
predicates.register("empty", empty)

predicates.register("closed", closed)
predicates.register("open", a(has("closed"), non("closed")))

#rule declaration

@after
@given(a("open", "empty", "container"))
def printed_name(e):
  return "(empty)"

```


## pretty good input parsing

```python
verbs.register("write", "write|inscribe", {"past":"wrote"})

verbs.register_structure("write", "{1:text}on|in{2}","{1:text}on|in{2}with|using{3}")
```

## standard library of modules
* core concepts like rooms/containers/scope use the above systems and can be removed, modified or redefined.

WIKI
======
[https://github.com/selfsame/mud.tilde.town/wiki](https://github.com/selfsame/mud.tilde.town/wiki)


Requirements
================
mud.tilde.town requires: 
* python 2.x
* [twisted https://twistedmatrix.com/trac/](https://twistedmatrix.com/trac/)
* [zope.interface https://pypi.python.org/pypi/zope.interface#download
](https://pypi.python.org/pypi/zope.interface#download)


