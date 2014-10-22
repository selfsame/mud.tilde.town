from colors import *

def intro(self):
        tb = background('red')
        cb = background('cyan')
        intro = [   background("cyan") + color("yellow") +
                    "            _____     _                 _      __  __ _    _ _____              ",
                    "           "+tb+"|_   _|"+cb+"   "+tb+"| |"+cb+"               "+tb+"| |"+cb+"    "+tb+"|  \/  | |"+cb+"  "+tb+"| |  __ \\"+cb+"             ",
                    "             "+tb+"| |"+cb+"  ___"+tb+"| |"+cb+" __ _ _ __   __"+tb+"| |"+cb+" ___"+tb+"| \  / | |"+cb+"  "+tb+"| | |"+cb+"  "+tb+"| |"+cb+"            ",
                    "             "+tb+"| |"+cb+" "+tb+"/ __| |/ _` | '_ \\"+cb+" "+tb+"/ _` |/ __| |\/| | |"+cb+"  "+tb+"| | |"+cb+"  "+tb+"| |"+cb+"            ",
                    "            _"+tb+"| |"+cb+"_"+tb+"\__ \ | ("+cb+"_"+tb+"| | |"+cb+" "+tb+"| | ("+cb+"_"+tb+"| |\__ \ |"+cb+"  "+tb+"| | |"+cb+"__"+tb+"| | |"+tb+"__| |"+cb+"            ",
                    "           "+tb+"|_____|___/_|\__,_|_|"+cb+" "+tb+"|_|\__,_||___/_|"+cb+"  "+tb+"|_|\____/|_____/"+cb+"             "+color('blue'),
                    "                                                    Created by Jplur            ",
                    "                                                                                ",
                    "     Ludum Dare #17 "+ color("green")+"              "+background("yellow")+"====="+background("cyan")+"  %#%                                    ",    
                    "  "+ color("white")+"     (Islands)   "+ color("green")+"             "+background("yellow")+"=== . ===#======="+background("cyan")+"       %                       ",    
                    "                               "+background("yellow")+"==  ..    #       =="+background("cyan")+"    %##%                     ",  
                    "                        %    #"+background("yellow")+"== ..           #   =="+background("cyan")+"   ##                       ", 
                    "                      %%#   %"+background("yellow")+"## ..            ##= . ===#=="+background("cyan")+"                      ",  
                    "                 %#  "+background("yellow")+"===#==== #.     ====    ==#=====     =="+background("cyan")+"                    ",  
                    "                  #"+background("yellow")+color('yellow')+",:=. ..;. .# =..=.=. =.=.==.#; . :.=.....=."+background("cyan")+"                  " + background("blue") + color("cyan"),  
                    "^*^^*^~~~*^^-*===  ... .... === ..~~~  ~~^ ==  ~~ ^ ==  ...====^*~^^*^~*^^~^~**~",
                    " * ^*~* ^^~ ^~*  ^ ~ * ^ ^ ^ ~~ ~ ^*~^^*^~*^^~~  ^^~  * ~ ^~ ^*~^ ^~*  ^~ ^~* *~",
                    "^ ^^ ^~~ *^^ ^^~ ^~*  .. ^^~ ^~* .~ ~~ ^^~ ^~* *~^^*^~*^^ . ^^~ *~^^ ^~*^ ~^~* ~",
                    background("black")]
        for entry in intro:
            self.sendLine(entry)
        self.sendLine("     Welcome to " + color("green") + "IslandsMUD" + color("white") + "!" )
        self.sendLine("     There are "+str( len( self.factory.clientProtocols ) )+" people online.")
        self.sendLine("     Type HELP in game for commands")
        self.sendLine("     ------------------------------------------")
        self.sendLine("please enter your name:")
        self.transport.write(">")
