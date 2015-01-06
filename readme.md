mud.tilde.town
==============

***A python MUD influenced by Inform7***

![](http://www.selfsamegames.com/screens/ttmud.png)



#Features

## Inform7 style function dispatching::
* Actions are a family of functions with lifecycle variations (check, before, during, after)
* Action calls are dipatched by arg arity, lifecycle version, and boolean predicate functions called on the arguments provided.
* Rich behavior trees are easily created by covering basic functionality then narrowing down edge cases to augment/ovveride.
* Behaviour is distributed, and easily alterable from separate modules.

```python
@action
@given(entity, a(closed, container))
def close(a, b):
  say("It's already closed.")

@action
@given(entity, a(opened, container))
def close(a, b):
  b["closed"] = True
  say("You close the "+name(b)+".")
  return True
```

## component entity system:
* data based game objects, loaded from json and converted to python dicts.
* components are defined as key value pairs.
* Constructing/serializing/merging functions easily declared for components.
* Entity definitions can have multiple ancestors.
* Directory structure of entity .json can declare inheritance via ```_base_.json``` files


```json
{"id":"treehouse",
"name":"a small treehouse.",
"desc":"It's tiny and crudely built.",
"exits": {"down": "lobby"},
"contents":[
	{"id":"chest", 
	 "name":"chest",
	 "closed":true,
	 "contents":[
		{"id":"coinpurse",
		 "contents":[{"id":"coin"},
					 {"id":"coin"}]}]}]}
```


## Schemaless
* rooms, objects, and entities are arbitrary components for the demo library.
* Games are defined by actions and entities, gameplay code is decoupled from the server

WIKI
======
There is a rather thourough set of documentation in the wiki:
[https://github.com/selfsame/mud.tilde.town/wiki](https://github.com/selfsame/mud.tilde.town/wiki)


Requirements
================
mud.tilde.town requires: 
* python 2.x
* [twisted https://twistedmatrix.com/trac/](https://twistedmatrix.com/trac/)
* [zope.interface https://pypi.python.org/pypi/zope.interface#download
](https://pypi.python.org/pypi/zope.interface#download)


