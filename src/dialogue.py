import os
import pickle
import time
import hashlib
import binascii
import base64

from colors import *
import parse
import components

def errorize(s):
  return wrap(s, color('red'))
def successize(s):
  return wrap(s, color('green'))

def verify(hash, plaintext):
  if hash == hashlib.sha512(plaintext).hexdigest():
    return True
    return False


class Dialogue:
  def __init__(self, con):
    #we init with a pointer to the chatprotocol connection
    self.con = con
    #this will get overridden with the first dialogue state
    self.state = self.start
    #this is checked to end the dialogue (also can return False from a state)
    self.done = False

  def initial(self):
    return "dialogue begun.."

  def input(self, s):
    return self.state(s)

  def start(self, s):
    return False


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
      self.account = components.make.load_json('./players/'+self.name+'.json')
      self.state = self.verify
      #self.con.echo(False)
      return "welcome back "+self.name+"\r\nEnter your password:"
    except:
      self.state = self.choose_pass
      #self.con.echo(False)
      return "New account, enter your desired password (4+chars):"

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
        if components.make.save_json(account, './players/'+self.name+'.json'):
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
                self.done = True
                self.con.clear()
                self.con.sendLine(successize("logging in with "+choice['firstname']))
                self.con.enter_game(idx)
            except:
                return "invalid character choice"
            
            return False
        return "invalid choice"

class Character(Dialogue):
    def initial(self):
        self.con.clear()
        return "CHARACTER CREATION\r\nenter your first name:"


    def start(self, s):
        self.firstname = parse.first_word(s)
        self.state = self.getgender
        return "Choose a gender (m/f/o):"

    def getgender(self, s):
        print [s, parse.first_word(s)]
        sex = parse.first_word(s)
        if s in ["m","f","o"]:
            character = {'firstname':self.firstname, 'gender':sex}
            self.con.account['characters'].append( character)
            self.con.save()
            return self.con.add_dialogue(Account(self.con))
        return errorize("invalid choice, try again:")


