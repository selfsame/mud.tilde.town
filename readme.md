A MUD for tilde.town.
====================

This is a python MUD I had originally wrote for LD17 
http://ludumdare.com/compo/ludum-dare-17/?action=preview&uid=1066

It is flavored after http://en.wikipedia.org/wiki/Mordor_(MUD)
but is just a small set of the basics.

The theme of the MUD is pirate islands, but could easily change.

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

