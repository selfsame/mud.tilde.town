#!/usr/bin/env/python
import re
from colors import color, background

def sentances(s):
  return re.findall('([^.;]+[\.;])', s)

def blocks(sl):
  for s in sl:
    if len(s) > 0:
      term = s[-1]
      if term == ".":
        print "sentance: " + s[0:-1]
      elif term == ";":
        print "block: " + s[0:-1]

def separate(pattern, s):
  rs = re.findall(pattern, s)
  res = re.split(pattern, s)
  return (rs, res)

def handlebars(s):
  unzip = separate('\{[^\{\}]*\}', s)
  swap = evalbars(unzip[0])
  zipped = [val for pair in zip(unzip[1], swap) for val in pair]
  return "".join(zipped)

def evalbars(l):
  resl = []
  for s in l:
    res = s[1:-1]
    if res[0:1] == "#":
      res = color(res[1:])
    resl.append(res)
  return resl


def parse(s):
  m = re.match(r"(?P<count>\d+)(d(?P<sides>\d+))*(\+(?P<plus>\d+))*", s)
  m2 = re.search(r"(\w+[\s:;.]+)*", s)
  return m2


def Main():
  p = sentances("Cats like dogs. To print the name of something (called S): get the name of S; and finish.")
  if p:
    b = blocks(p)
    print b
  print handlebars("The {#green}cat{#reset} likes {friend of this}, {#red}but not{#white} {enemy of this}.")

if __name__== '__main__' :Main()
