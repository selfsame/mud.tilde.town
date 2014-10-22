from functions import formatinput
from colors import *

def create(self, line, state):
    #going to use self.new as our index for progress
    #since it's allready set up
    line = formatinput(line)
    splitline = line.lower().split(" ")

    if line == "m":
        self.sex = "m"
        state = 2
    elif line == "f":
        self.sex = "f"
        state = 2
    elif line == "o":
        self.sex = "o"
        state = 2
    else:
        self.sendLine("illegal name, try again:")
        self.protocol.transport.write(">")
    if state == 2:
        return 1
