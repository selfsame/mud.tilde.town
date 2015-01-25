from mud.core import *
from colors import color
from mud.core.util import *
from mud.core.CAPSMODE import *


bind.verb("look", "look at|look|l|examine|x")
bind.verb("take", "get|take|grab|pick up")

bind.verb("give", "give|hand")
bind.verb("close", "close|shut")
bind.verb("open", "open")
bind.verb("walk", "go|enter|leave|walk")
bind.verb("quit", "quit")
bind.verb("save", "save", {"doc":"Saves the character."})
bind.verb("inventory", "inventory|inv|i")

bind.verb("drop", "drop|put|place|set|throw")
bind.verb_pattern("drop", "{1}inside (of)?|in(to)?{2}","{1}")

bind.verb("talk", "say|[\']", {"past":"said"})
bind.verb_pattern("talk", "{1:text}to{2}", "{1:text}")

bind.verb("tell", "tell", {"past":"told"})
bind.verb_pattern("tell", "{1} [\'\"]*{2:text}[\'\"\?]*")

bind.verb("ask", "ask", {"past":"asked"})
bind.verb_pattern("ask","{1}:{2:text}", "{1:text}")

