import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import parse
from components import instance, register
from util import *
from actions import *
import data
from colors import *
from verbs import determine
import re
from predicates import string, container

DEBUG = False
def debug(*args):
  if DEBUG:
    print "debug",args

def recursive_register(e):
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
    self.input("look")
    self.prompt()
  

  def update(self, delta):
    pass

  def send(self, s):
    self.con.sendLine(s)

  def input(self, line):
    data.subject = self.data
    directive = determine(line)
    debug(directive)
    if len(directive) > 0:
      verb = directive[0]
    else:
      debug("NO DIRECTIVE")
      return
    if len(directive) == 1:
      debug("single verb statement:", verb)
      act(verb, self.data)
      data.subject = {}
      return

    res = []

    scope = False
    holders = False
    holder_conts = False
    matches = []
    for part in directive[1:]:
      if part[0] and part[1]:
        if part[0] == "arg":
          res.append(part[1])
        if part[0] == "container":
          if scope == False:
            scope = act("check_scope_while", self.data, verb) or []

          #search scope for matching containers
          #find best matches
          debug("matching "+part[1]+"to a container..")
          holder_string = part[1]
          hs = filter(container, scope)
          holders = scope_matches(hs, holder_string)
          debug("matched: ", map(name, holders))
          report = ""
          holder_conts = []
          for h in holders:
            report += name(h)+"\r\n"
            for c in contents_of(h):
              report += "  "+name(c)+"\r\n"
            holder_conts += contents_of(h)
          
          debug("HOLDERS:\r\n", report)
        if part[0] == "noun":
          noun_string = part[1]
          debug("SEARCHING FOR: ", noun_string)
          if holder_conts:
            matches = scope_matches(holder_conts, noun_string)
            debug("HOLDER MATCHES: ", map(name, matches))
          if len(matches) == 0:
            if scope == False:
              scope = act("check_scope_while", self.data, verb) or []
            elif len(res) == 1:
              scope = act("check_scope_while", self.data, verb, "loc") or []
            matches = scope_matches(scope, noun_string)
            debug("NOUN MATCHES: ", map(name, matches))
          matches.append(None)
          if len(matches) > 0:
            res.append(matches[0])
            matches = []

    
    debug("FINAL:", [verb] + map(name, res))
    data.subject = self.data
    apply(act, ["player_command", verb, self.data] + res)
    apply(act, [verb, self.data] + res)


  def prompt(self):
    self.con.transport.write(act("line_prompt", self.data))

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
    act("delete", self.data)
    self.con.factory.broadcast(color("magenta")+self.data['firstname']+" has disconnected."+color("reset"))
    self.con.close_connection("QUITTING!")

  def _quit(self):
    act("quit", self.data)

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


