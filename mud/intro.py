from core.colors import *
from core import dialogue

class Intro(dialogue.Dialogue):
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
      return self.con.add_dialogue(dialogue.Login(self.con))
    if s == "2":
      return  self.con.close_connection("goodbye!")
    if s == "3":
      self.done = False
      return "0 players online"
    self.done = False
    return color('red')+"unknown choice, try again"+color('reset')
