mud.tilde.town
==============

![](http://www.selfsamegames.com/screens/ttmud.png)

***A python MUD influenced by Inform7***

## component entity system:
* data based game objects, loaded from json.
* Composable entitiy dictionaries can use multiple inheritances, or merge and recombine as desired.
* Constructing/serializing component functions easily declared
* Can be constructed dymanically

```json
{"id":"treehouse",
"name":"a small {#green}treehouse{#reset}.",
"desc":"It's tiny and crudely built.",
"exits": {"down": "lobby"}
"contents":[
	{"id":"chest", "name":"chest",
	"contents":[
		{"id": "note", "name":"memo",
		 "desc":"The 'contents' component will merge partial data with an instance of the full 'id' entry"},
		{"id":"coinpurse",
		 "contents":[{"id":"coin"},
					 {"id":"coin"},
					 {"id":"coin"}]}]}]}
```

## Inform7 style predicate/arity dispatch 'action' functions:
* Actions are a family of function lifecycle variations (check, before, during, after)
* Action calls are dipatched by arg arity, lifecycle version, and boolean functions called on the arguments provided.
* python decorators hold the declarations
* Rich behavior trees are easily created by covering basic functionality then narrowing down edge cases to augment/ovveride

```python
@after
@given(player, container)
def look(p, r):
  say("Inside it you see "+ act("list_contents", p, r)+ ".")

@after
@given(player, a(empty, container))
def look(p, r):
  say("It's completely empty.")
```

## Schemaless
* rooms, objects, and entities are arbitrary components for the demo library
* Game class pumps updates to some component(s), which propigate the game loop via Actions
* Player class handles login authentication and links into the game system with entity proxies




Connecting
===========

On tilde.town, you can connect with
```
telnet localhost 5071
```

Requirements
================
mud.tilde.town requires: 
* python 2.x
* twisted https://twistedmatrix.com/trac/
* zope.interface https://pypi.python.org/pypi/zope.interface#download

All requirements are installed on tilde.town, so you can simple clone the repo
and run
```
python server.py {port number}
```
where port number is an open port (try something between 5000-9000)

WIKI
======
[https://github.com/selfsame/mud.tilde.town/wiki](https://github.com/selfsame/mud.tilde.town/wiki)

