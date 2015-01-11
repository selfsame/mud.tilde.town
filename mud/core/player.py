import parse
from data import instance, register
from util import *
from dispatch import *
import data
from colors import *
from mud.core import verbs
import re
from mud.core.predicates import string
from mud.game.standard import predicates

__all__ = ["Player"]


DEBUG = False

def debug(*args):
  if DEBUG:
    print " ".join(map(str, args))

def recursive_register(e):
  if isinstance(e, str): 
    return e
  cont = e.get("contents")
  if cont:
    e["contents"] = map(recursive_register, cont)
  register(e)
  return e.get("uuid")


class Player():
  def __init__(self, con, d):
    entity = instance("player")
    self.con = con
    self.data = dict(entity.items() + d.items())
    self.data['player'] = self
    recursive_register(self.data)
    if not self.data.get('located'):
      self.data['located'] = "lobby"
    r = data.rooms.get(self.data['located'])
    r['contents'].append(self.data['uuid'])
    data.subject = self.data
    call("init", self.data)
    self.input("look")
    self.prompt()

  def send(self, s):
    self.con.sendLine(s)

  def input(self, line):
    data.subject = self.data
    directive = verbs.determine(line)
    debug(directive)
    if len(directive) > 0:
      verb = directive[0]
    else:
      debug("NO DIRECTIVE")
      return
    if len(directive) == 1:
      debug("single verb statement:", verb)
      call(verb, self.data)
      data.subject = {}
      return

    res = []
    rest = directive[1:]
    default_scope = False
    if rest:
      for idx, part in enumerate(rest):
        if "text" in part:
          res.append(part["text"])
        elif "noun" in part:
          argscope = call("scope_"+str(idx+1)+"_while", self.data, verb)
          if not argscope:
            if not default_scope:
              default_scope = call("scope_while", self.data, verb)
          scope = argscope or default_scope or []
          if DEBUG:
            print "SCOPE:"
            for thing in scope:
                print "-"+name(thing)
            print " "
          s = part["noun"]["string"]
          if "holder" in part["noun"]:
            matches = find_held_scope(part["noun"], scope)
          else:        
            matches = scope_matches(scope, s)
          if matches:
            res.append(matches[0])
          else:
            res.append(s)
        else:
          res.append(None)

    debug("FINAL:", [verb] + map(name, res))
    data.subject = self.data
    if apply(call, ["object_blocked", verb, self.data] + [res]): return False
    apply(call, [verb, self.data] + res)


  def prompt(self):
    self.con.transport.write(call("line_prompt", self.data))

  def save(self,character):
    try:
      idx = self.con.character_idx
      self.con.account["characters"][idx] = character
      return self.con.save()
    except:
      return False

  def quit(self):
    if self.data in data.scope: data.scope.remove(self.data)
    if data.subject == self.data: data.subject = {}
    call("delete", self.data)
    self.con.factory.broadcast(color("magenta")+self.data['firstname']+" has disconnected."+color("reset"))
    self.con.close_connection("QUITTING!")

  def _quit(self):
    call("quit", self.data)

def not_none(e):
  if e != None: return True
  return False

def scope_matches(_scope, s):
  scope = filter(not_none, _scope)
  if not string(s): return []
  res = []
  regex = "thing"
  for e in scope:
    if string(e):
      regex = e
    elif e:
      regex = e.get('regex')
    else:
      print "Nonetype?", e, scope
    if string(regex):
      if re.match(regex, s):
        res.append(e)
    if s == name(e):
      res.append(e)
  return res

def get_holder_stack(cursor, stack=[]):
  stack = [cursor] + stack
  if "holder" in cursor:
    return get_holder_stack(cursor["holder"], stack)
  else:
    return stack

def find_held_scope(cursor, scope):
  stack = get_holder_stack(cursor["holder"])
  debug("STACK", stack)
  if stack:
    scopes = [scope]
    indent = "  "
    for item in stack:
      debug("->", item)
      paths = []
      for branch in scopes:
        hs = filter(predicates.get("container"), branch)
        matches = scope_matches(hs, item["string"])
        if matches:
          for m in matches:
            debug(indent+"-", name(m))
            paths.append(contents_of(m))
      scopes = paths
      indent += "  "
    res = []
    for branch in scopes:
      res += scope_matches(branch, cursor["string"])
    debug("FOUND", map(name, res))
    return res
