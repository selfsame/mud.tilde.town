mud.tilde.town*
==============
***python library for telnet interactive fiction***

![](http://www.selfsamegames.com/screens/showoff.png)

Requirements
================
* python 2.x
* [twisted https://twistedmatrix.com/trac/](https://twistedmatrix.com/trac/)
* [zope.interface https://pypi.python.org/pypi/zope.interface#download
](https://pypi.python.org/pypi/zope.interface#download)


#Features

## extensive function dispatching
[wiki - dispatching](https://github.com/selfsame/mud.tilde.town/wiki/rules)

[wiki - predicates](https://github.com/selfsame/mud.tilde.town/wiki/predicates)

* inspired by inform7
* functions dispatch for argument arity, argument predicate, and lifecycle variations (check, before, during, after)
* Rich behavior trees are easily created by covering basic functionality then narrowing down edge cases to augment/ovveride.
* functions and predicates are declarativly registered, avoiding import dependencies between game modules.
* predicates serve as a type system: core provides standard types ``` anything number integer string function sequential dictionary module undefined empty````
* predicate composition functions: ```a(symbol_pred, "bound_pred"), non("registered")``` make it easy to specify dispatch guards on the fly. ```equals(literal), has("key")``` also provided.


```python
@after(a("locked", "closed", "container"))
def print_name(e):
  return "(locked)"

@check("entity", a("closed", "container"))
def close(a, b):
  say("It's already closed.")
  return False

@given("entity", a("opened", "container"))
def close(a, b):
  b["closed"] = True
  say("You close "+act("indefinate_name", b)+".")
```

## component/entity game objects:
* python dicts are entities, key|vals are component types|values
* Constructing/serializing/merging functions easily declared for components.
* data based definitions, .json files or python dicts.
* entity definitions can extend from multiple ancestors.
* Directory structure of entity .json can declare inheritance via ```_base_.json``` files


```json
{"id":"chest",
"name":"wooden chest",
"descripton":"It is likely to have a thing or two inside",
"extends":["object"],
"contents":[{"id":"mouse","color":"random"}],
"color":"brown",
"capacity":5,
"closed":true,
"opaque":true}
```

```python
from mud.core import *
import random

@construct
def color(c):
  if c == "random":
    return random.choice(["brown","red","cyan"])
  return c

def _color_is(c): 
  def hue(e): return e.get('color') == c
  return hue

#binding predicates allows any other module to use or overwrite them
bind.predicate("colored", has('color'))
bind.predicate("brown", _color_is("brown"))
bind.predicate("red", _color_is("red"))
bind.predicate("cyan", _color_is("cyan"))

#binding adjectives, the standard/player/input.py module finds predicates from adjective strings to filter matches
bind.adjective("colored", "colored")
bind.adjective("red", "red")
bind.adjective("brown", "brown")
bind.adjective("cyan", "cyan")

#dispatching "printed_name" should be sandwiched by these rules
@before(a("cyan", "thing"))
def printed_name(e):
  return "{#bold}{#cyan}"

@before(a("brown", "thing"))
def printed_name(e):
  return "{#yellow}"

@before(a("red", "thing"))
def printed_name(e):
  return "{#red}"

@after(a("colored", "thing"))
def printed_name(e):
  return "{#reset}"

```

## extremely decoupled modules
* no import requirements between ```game/``` modules
* dispatch rules, component functions, predicates, verbs, adjectives all bound to strings and can be overwritten or removed.
* module load order determines dispatching and binding priority
* all game concepts built from standard modules, easy to drastically change the core design of a game




## input parsing
[wiki - player input and verbs](https://github.com/selfsame/mud.tilde.town/wiki/verbs)

verbs can have multiple gramatical forms with arbitrary argument count and ordering.

The standard game modules (```standard/player``` and ```standard/scope```) handle resolution of captured strings to entities or values.

```python
verbs.register("write", "write|inscribe", {"past":"wrote"})

verbs.register_structure("write", "{1:text}on|in{2}","{1:text}on|in{2}with|using{3}")
```



## contextualized string templates
[wiki - context and reporting](https://github.com/selfsame/mud.tilde.town/wiki/context)

subject, verb, objects, and observing scope can be set and rewound with ```mud.core.context```'s ```understood```

Text can easily be customized for the observer, (especially useful to refer to acting player as "you|yourself")
```python
#player commands have proper context.understood, 
#but this can be changed and reverted incrementally if needed
understood.subject(e)

report("[Subject] introduce[s] [itself] to [object].")

#undoes the previous subject change 
understood.previous()
```



## colorcode templates with nesting foreground/background colors
```parse.template``` tracks fg/bg color stacks, allowing you to nest colorcoded strings. ```parse``` also includes utilities for getting length, indicies, and splices of a templated string.
```
parse.template("{%green}bg-green{#yellow}fg-yellow {#red}fg-red {#magenta}fg-magenta{%reset}bg-default{#reset}fg-red {#reset}fg-yellow {#reset}fg-default")
```




MORE WIKI
======
[https://github.com/selfsame/mud.tilde.town/wiki](https://github.com/selfsame/mud.tilde.town/wiki)





