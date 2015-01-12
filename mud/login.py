import os, hashlib, binascii, base64

from core.colors import *
from core.dialogue import Dialogue
from core import parse
from core import data

def errorize(s):
  return wrap(s, color('red'))
def successize(s):
  return wrap(s, color('green'))

def verify(hash, plaintext):
  if hash == hashlib.sha512(plaintext).hexdigest():
    return True
    return False

class Intro(Dialogue):
  def initial(self):
        tb = background('red')
        cb = background('cyan')
        intro = [   color("bold")+background("cyan") + color("yellow") +
                    "           "+   " _____ "+   "    _                 _      __  __ _    _ _____              ",
                    "           "+tb+"|_   _|"+cb+"   "+tb+"| |"+cb+"               "+tb+"| |"+cb+"    "+tb+"|  \/  | |"+cb+"  "+tb+"| |  __ \\"+cb+"             ",
                    "             "+tb+"| |"+cb+"  ___"+tb+"| |"+cb+" __ _ _ __   __"+tb+"| |"+cb+" ___"+tb+"| \  / | |"+cb+"  "+tb+"| | |"+cb+"  "+tb+"| |"+cb+"            ",
                    "             "+tb+"| |"+cb+" "+tb+"/ __| |/ _` | '_ \\"+cb+" "+tb+"/ _` |/ __| |\/| | |"+cb+"  "+tb+"| | |"+cb+"  "+tb+"| |"+cb+"            ",
                    "            _"+tb+"| |"+cb+"_"+tb+"\__ \ | ("+cb+"_"+tb+"| | |"+cb+" "+tb+"| | ("+cb+"_"+tb+"| |\__ \ |"+cb+"  "+tb+"| | |"+cb+"__"+tb+"| | |"+tb+"__| |"+cb+"            ",
                    "           "+tb+"|_____|___/_|\__,_|_|"+cb+" "+tb+"|_|\__,_||___/_|"+cb+"  "+tb+"|_|\____/|_____/"+cb+"             "+color('blue'),
                    "                                                    tild.town's official MUD!   ",
                    "                    "+ color("green")+"              "+background("yellow")+"====="+background("cyan")+"  %#%                                    ",    
                    "  "+ color("white")+"     (Islands)   "+ color("green")+"             "+background("yellow")+"=== . ===#======="+background("cyan")+"       %                       ",    
                    "                               "+background("yellow")+"==  ..    #       =="+background("cyan")+"    %##%                     ",  
                    "                        %    #"+background("yellow")+"== ..           #   =="+background("cyan")+"   ##                       ", 
                    "                      %%#   %"+background("yellow")+"## ..            ##= . ===#=="+background("cyan")+"                      ",  
                    "                 %#  "+background("yellow")+"===#==== #.     ====    ==#=====     =="+background("cyan")+"                    ",  
                    "                  #"+background("yellow")+color('yellow')+",:=. ..;. .# =..=.=. =.=.==.#; . :.=.....=."+background("cyan")+"                  " + background("blue") + color("cyan"),  
                    "^*^^*^~~~*^^-*===  ... .... === ..~~~  ~~^ ==  ~~ ^ ==  ...====^*~^^*^~*^^~^~**~",
                    " * ^*~* ^^~ ^~*  ^ ~ * ^ ^ ^ ~~ ~ ^*~^^*^~*^^~~  ^^~  * ~ ^~ ^*~^ ^~*  ^~ ^~* *~",
                    " ^ ~ . ~ .^.^ "+color('magenta')+"(1)login"+ color("cyan")+"  ^ .~ ^* .~ "+color('magenta')+"(2)quit"+ color("cyan")+"  *. ^ ~ .* "+color('magenta')+"(3)who"+color('cyan')+" * ~. ^  ^ . ^ ~ ",
                    "^ ^^ ^~~ *^^ ^^~ ^~*  .. ^^~ ^~* .~ ~~ ^^~ ^~* *~^^*^~*^^ . ^^~ *~^^ ^~*^ ~^~* ~",

                                        background("reset")]
        return "\r\n".join(intro)
  
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
    return color('red')+"unknown choice, try again"+color('reset')


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