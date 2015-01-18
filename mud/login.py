import os, hashlib, binascii, base64

from core.colors import *
from core.dialogue import Dialogue
from core import parse
from core import data

def errorize(s):
  return wrap(s, color('magenta'))
def successize(s):
  return wrap(s, color('magenta'))

def verify(hash, plaintext):
  if hash == hashlib.sha512(plaintext).hexdigest():
    return True
    return False






                                                                          
                                                                          

class Intro(Dialogue):
  def initial(self):
    intro = [
"{#bold}{%blue}{#yellow}  o                       .                       .                             ",
"{#bold}                 .                    {%black}/\{%reset}                       o                ",
"{#bold}    .                            o  _{%black}/  \{%reset}                                       ",
"{#bold}                    .         _    {%black}/     \{%reset}_             .            .          ",
"{#bold}          o                  {%black}/ \{%reset}  {%black}/        \{%reset}    {%black}/\{%reset}                              ",
"{#bold}                            {%black}/   \/          \{%reset}  {%black}/  \{%reset}       . ,                  o",
"{#bold}                        {%black}/\{%reset}_{%black}/                 \/    \{%reset}_     .0                    ",
"{#bold}           .      _    {%black}/         _ _     _           \{%reset}     '`             .     ",
"{#bold}    .            {%magenta}| |{%reset}  {%black}/     _   {%magenta}(_) |{%reset}   {%magenta}| |{%reset}           \{%reset}_ _      .               ",
"{#bold}  ____  _   _  _ {%magenta}| |{%reset} {%black}/     {%magenta}| |{%reset}_  _{%magenta}| |{%reset} _ {%magenta}| |{%reset} ____        {%magenta}| |{%reset}{%reset}_  ___  _ _ _ ____   ",
"{#bold} {%magenta}|    \| |{%reset} {%magenta}| |/ || |{%reset}{%black}/      {%magenta}|  _)| | |/ || |/ _  ){%reset}       {%magenta}|  _)/ _ \| | | |  _ \{%reset}{%reset}  ",
"{#bold} {%magenta}| | | | |{%reset}_{%magenta}| ( ({%reset}_{%magenta}| |{%reset}{%black}   _   {%magenta}| |{%reset}__{%magenta}| | ( ({%reset}_{%magenta}| ( (/ /{%reset}    _   {%magenta}| |{%reset}{%reset}_{%magenta}| |{%reset}_{%magenta}| | | | | |{%reset} {%magenta}| |{%reset} ",
"{#bold} {%magenta}|_|_|_|\____|\____|{%reset}{%black}  {%magenta}(_){%reset}   {%magenta}\___)_|_|\____|\____){%reset}  {%magenta}(_){%reset}  {%magenta} \___)___/{%reset}{%reset} {%magenta}\____|_|{%reset} {%magenta}|_|{%reset} ",
"{#bold}                 {%black}/                              _            \{%reset}     {%black}/  \{%reset}         ",
"{#bold}                {%black}/         /\                   / \         /\ \{%reset}   {%black}/    \{%reset}  {%black}/\{%reset}    ",
"{#bold} o     _{%black}/\{%reset}    _{%black}/         /  \  /\             /           /  \_\{%reset}_{%black}/      \/  \{%reset}   ",
"{#bold}      {%black}/   \{%reset}__{%black}/               \/  \_    {#bold}{#red}{#bold}     __ {#reset}                       __/    \{%reset}_{%black}/{%reset}",
"{#bold}    _{%black}/      \                 \    \ {#bold}{#red}{#bold}    __{%blue}| -|{%reset}__           {#reset}         /        \{%reset}_",
"{#bold}   {%black}/         \_ {#bold}{#red}{#bold}           _____        {%blue}|- -| - -|{%reset}_         {#reset}                    {%reset}",
"{#bold} _{%black}/             {#bold}{#red}{#bold}      ____{%blue}|- - -|{%reset}_   ___{%blue}|_  |- |- -|{%reset}  __    _  .{#reset}  {%green}{#black}#{#reset}{%reset}    {#green}%{#reset}        {%reset}",
"{%black}/   .{#green}%{#reset}''  ` {#green}%~{#reset}. {#bold}{#red}{#bold} __{#green}+{#reset}_{%blue}| D  |  D| D |{%reset} {%blue}| D   |D| D|  D|{%reset}_{%blue}|D |{%reset}{#green}%{#reset}_{%blue}|D|{%reset}____ ^{#reset} {#green}%{#reset} {%green}{#black}#{#reset}{%reset}~  {%green}{#black}#{#reset}{%reset} ` {%green}{#black}#{#reset}{%reset}{%reset}",
"{%black}. {#green}%'{#reset}.{%green}{#black}#{#reset}{%reset} .{#green}%{#reset} . ^{%green}{#black}#{#reset}{%reset}^  . ~ , {#green},%.{#reset}.  .`   / \  . ~.    {#green}%{#reset}  ^      ^ {#green}%{#reset}  ^ {%green}{#black}#{#reset}{%reset} ^   {%green}{#black}#{#reset}{%reset}    ^   {%reset}{%reset}{#reset}{#reset}{#reset}{#reset}{#reset}",
"   .   ,      `                                                  .   ~  .      ,",
"~         .    ({#yellow}{#bold}1{#reset} {#magenta}login{#reset})         ({#yellow}{#bold}2{#reset} {#magenta}quit{#reset})         ({#yellow}{#bold}3{#reset} {#magenta}who{#reset})      `   .    "]

    return parse.template("\r\n".join(intro))
  
  def start(self, s):
    self.done = True
    if s == "1":
      return self.con.add_dialogue(Login(self.con))
    if s == "2":
      return  self.con.close_connection("goodbye!")
    if s == "3":
      self.done = False
      return "0 players online"
    self.done = False
    return color('magenta')+"unknown choice, try again"+color('reset')


class Login(Dialogue):
  def start(self, s):
    self.passw = False
    self.name = parse.first_word(s)
    if len(self.name) < 2:
      return "account names must be at least two characters long and only use alphabetical chars!\r\nEnter your name:"
    elif self.name.lower() in ['look', 'get', 'kill', 'kil','loo', 'who', 'help']:
      return self.name+" is a reserved word\r\n Enter your name:"
    try:
      print ("checking for "+self.name+".sav")
      self.account = data.load_json('./save/accounts/'+self.name+'.json')
      self.state = self.verify
      #self.con.echo(False)
      return "welcome back "+self.name+"\r\nEnter your password:"
    except Exception as exc:
      print exc
      self.state = self.choose_pass
      #self.con.echo(False)
      return "New account, enter your desimagenta password (4+chars):"

  def initial(self):
    return "logging in...\r\nEnter your name:"

  def verify(self, s):
    passw = s
    if verify(self.account['password'], self.account['salt'] + passw):
      self.done = True
      self.con.account = self.account
      #self.con.echo(True)
      return self.con.add_dialogue(Account(self.con))
    else:
      self.con.close_connection(errorize("INCORRECT - CLOSING CONNECTION"))

  def choose_pass(self, s):
    if self.passw:
      if s == self.passw:
        #self.con.echo(True)
        account = {'name':self.name, 'salt':base64.b64encode(os.urandom(16)), 'characters':[], 'email':False}
        account['password'] = hashlib.sha512(account['salt'] + self.passw).hexdigest()
        if data.save_json(account, './save/accounts/'+self.name+'.json'):
            print "account created: "+self.name
        self.con.account = account
        return self.con.add_dialogue(Account(self.con))
      else:
        self.passw = False
        return errorize("password mismatch!\r\n")+"Choose a password:"
    else:
      self.passw = s
      return "re-enter your password:"

class Account(Dialogue):
    def initial(self):
        self.con.clear()
        account = self.con.account
        message = [
        "+-------------------------------------+",
        "|ACCOUNT : "+wrap(" "+str(account['name'])+" ", background('blue')),
        "+-------------------------------------+",
        "| "+wrap(" new)", color('magenta'))+" Create a new character",
        "| "+wrap("quit)", color('magenta'))+" Close your connection",
        "+-------------------------------------+"]

        chars = ["| choose a character: "]
        i = 0
        for c in account['characters']:
            chars.append( "| "+wrap(str(i)+") ", color('magenta'))+c['firstname'])
            i += 1
        if len(chars) > 1:
            message += chars
        message = "\r\n".join(message)
        return message

    def start(self, s):
        self.firstname = ""
        if s.lower() == "new":
            return self.con.add_dialogue(Character(self.con))
        elif s.lower() == "quit":
            self.con.close_connection("goodbye!")
        else:
            try:
              idx = int(s)
              choice = self.con.account['characters'][idx]
            except Exception as exc:
              print exc
              return "invalid choice"
            self.done = True
            self.con.clear()
            self.con.sendLine(successize("logging in with "+choice['firstname']))
            self.con.enter_game(idx)
            return False
        return "invalid choice"

_origins = {
"a city orphan that was raised by the streets.":{
  "stats":{
    "dex":4,
    "con":-2,
    "int":-4},
  "skills":{
    "eloquence":-10,
    "stealth":15,
    "literacy":-30,
    "brawling":20,
    "climbing":15},
  "perks":{"nickname", "insecure"}
  },
"the bastard child of a fishwife.":{
  "stats":{
    "str":2,
    "con":1,
    "int":-1,
    "dex":-2},
  "skills":{
    "sealore":15,
    "knives":20},
  "perks":{"fatherless"}
  },
"a farmers child, youngest of 6.":{
  "stats":{
    "str":5,
    "con":2,
    "int":-4,
    "dex":-1},
  "skills":{
    "eloquence":-20,
    "plantlore":20
    },
  "perks":{"honest"}
  },
"only child to a textile merchant.":{
  "stats":{
    "str":-2,
    "con":-2,
    "int":4,
    "dex":-1},
  "skills":{
    "eloquence":5,
    "literacy":20,
    "clothlore":20},
  "perks":{"handsome"}
  },
"under the strict rule of your father, a Brigadier General.":{
  "stats":{
    "str":1,
    "con":1,
    "int":1,
    "dex":-2},
  "skills":{
    "eloquence":-5,
    "literacy":10,
    "weaponlore":10},
  "perks":{"proud", "unfriendly"}
  },
"favorite child of a Gypsy king.":{
  "stats":{
    "str":-3,
    "int":3,
    "dex":3},
  "skills":{
    "eloquence":15,
    "stealth":6,
    "literacy":-10,
    "weaponlore":5},
  "perks":{"friendly", "lucky", "nickname"}
  },
"grandchild of an impoverished Baroness.":{
  "stats":{
    "str":-1,
    "int":2,
    "dex":1},
  "skills":{
    "eloquence":25,
    "stealth":-10,
    "literacy":20,
    "weaponlore":-15,
    "horselore":12},
  "perks":{"clumsy"}
  },
"only child of a sailor, lost at sea before you turned eight.":{
  "stats":{
    "str":2,
    "int":-2,
    "dex":1},
  "skills":{
    "sealore":25,
    "stealth":5,
    "literacy":-5,
    "weaponlore":5,
    "climbing":20,
    "swimming":10,
    "shooting":4},
  "perks":{"unlucky"}
  },
"a groundskeepers child who had the run of the master's estate.":{
  "stats":{
    "str":2,
    "dex":1,
    "con":-1,
    "int":-2},
  "skills":{
    "eloquence":6,
    "stealth":5,
    "literacy":-8,
    "weaponlore":8,
    "climbing":10,
    "swimming":8,
    "plantlore":5,
    "animallore":10,
    "shooting":7,
    "horselore":6},
  "perks":{"homely", "honest"}
  },
"the butchers sickly child.":{
  "stats":{
    "con":-4},
  "skills":{
    "meatlore":50},
  "perks":{"butcherborn"}
  }}

class Character(Dialogue):
    def initial(self):
        self.con.clear()
        self._origins = _origins.items()
        message = "CHARACTER CREATION:\r\n\r\nYou started life.."+"\r\n    "
        for idx, o in enumerate(self._origins):
          message += "\r\n  ("+str(idx)+") "+o[0]
        return message

    def start(self, s):
        
        try:
          self.character = self._origins[int(parse.first_word(s))][1]
          self.state = self.firstname
          return "Enter your characters first name:"
        except:
          return "invalid choice\r\n>"

    def firstname(self, s):
        n = parse.first_word(s).lower()
        if len(n) < 3: return "First names must be 3 letters or more, retry:"
        self.firstname = n[0].upper()+n[1:]
        self.state = self.lastname
        return "Enter your characters last name:"

    def lastname(self, s):
        n = parse.first_word(s).lower()
        if len(n) < 3: return "Last names must be 3 letters or more, retry:"
        self.lastname = n[0].upper()+n[1:]
        self.state = self.getgender
        return "Choose a gender (m/f/o):"

    def getgender(self, s):
        print [s, parse.first_word(s)]
        sex = parse.first_word(s)
        if s in ["m","f","o"]:
            self.character['perks'] = list(self.character['perks'])
            self.character['firstname'] = self.firstname
            self.character['lastname'] = self.lastname
            self.character['gender'] = sex
            self.con.account['characters'].append(self.character)
            self.con.save()
            return self.con.add_dialogue(Account(self.con))
        return errorize("invalid choice, try again:")