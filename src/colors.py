## ANSI color helper

def color(name):
    codes = {  "reset" :   "\033[01;00m",
               "bold" :   "\033[01;01m",
               "boldoff" :   "\033[01;22m",
                "blue"  :   "\033[01;34m",
                "black" :   "\033[01;30m",
                "red"  :   "\033[01;31m",
                "green"  :   "\033[01;32m",
                "yellow"  :   "\033[01;33m",
                "magenta"  :   "\033[01;35m",
                "cyan"  :   "\033[01;36m",
                "white"  :   "\033[01;37m", }
    return codes[name]

def background(name):
    codes = {  "reset" :   "\033[01;00m",
               "bold" :   "\033[01;01m",
               "boldoff" :   "\033[01;22m",
                "blue"  :   "\033[01;44m",
                "black" :   "\033[01;40m",
                "red"  :   "\033[01;41m",
                "green"  :   "\033[01;42m",
                "yellow"  :   "\033[01;43m",
                "magenta"  :   "\033[01;45m",
                "cyan"  :   "\033[01;46m",
                "white"  :   "\033[01;47m", }
    return codes[name]

def wrap(s, c):
    return c+s+color('reset')+background('reset')
