#!/usr/bin/env/python
import re
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
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
  rs = re.findall(pattern, s) + [""]
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
    elif res[0:1] == "%":
      res = background(res[1:])
    resl.append(res)
  return resl


def parse(s):
  m = re.match(r"(?P<count>\d+)(d(?P<sides>\d+))*(\+(?P<plus>\d+))*", s)
  m2 = re.search(r"(\w+[\s:;.]+)*", s)
  return m2


def Main():
  print handlebars("The {#green}cat{#reset} sat on a box.")



if __name__== '__main__' :Main()



