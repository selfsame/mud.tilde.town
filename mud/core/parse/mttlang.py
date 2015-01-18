#!/usr/bin/env/python
import re
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from colors import color, background
from CAPSMODE import *


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

def removebars(s):
  return "".join(separate('\{[^\{\}]*\}', s)[1])

def template_index(s, i):
  if isinstance(s, str):
    s = separate('\{[^\{\}]*\}', s)
  ti = 0
  pi = 0
  for idx, part in enumerate(s[1]):
    plen = len(part)
    if i > pi + plen:
      pi += plen
      ti += len(s[0][idx])
    else:
      partial = plen - ((pi + plen) - i) 
      return ti + pi + partial
  return ti + pi


def temp_slice(s, start=None, end=None):
  sep = separate('\{[^\{\}]*\}', s)
  if start:
    tstart = template_index(sep,start)
  if end:
    tend = template_index(sep,end)
  if start:
    if end:
      return s[tstart:tend]
    return s[tstart:]
  if end:
    return s[:tend]
  return s


def tokens(data, t):
  if t == "": 
    data["codes"].append("")
    return data
  t = t[1:-1]
  # if tag == "bold":
  #   if not GET(data,"bold"):
  #     data["bold"] = True
  #     data["codes"].append(color("bold"))
  if t[0] == "#":
    tag = t[1:]
    try:
      code = color(tag)
      data["c"].append(tag)
      data["codes"].append(code)
      if tag == "reset":
        if GET(data["b"], -1):
          data["codes"].append(background(GET(data["b"], -1)))
          pass
    except: pass
  if t[0] == "%":
    tag = t[1:]
    try:
      code = background(tag)
      data["b"].append(tag)
      data["codes"].append(code)
      if tag == "reset":
        if GET(data["c"], -1):
          data["codes"].append(color(GET(data["c"], -1)))
          pass
    except: pass
  return data



def evalbars(l):
  resl = []
  duct = reduce(tokens, l, {"codes":[],"c":[],"b":[]})
  return duct["codes"]

def words(s):
  sep = separate('\{[^\{\}]*\}', s)
  m =  re.findall('(([\w\(\)\.,]*\{[^\{\}]*\}[^ \{]*)+([\w\(\)\.,]*)|([\w\(\)\.,]+))', s)
  return map(lambda x: x[0], m)

def length(s):
  return len("".join(separate('\{[^\{\}]*\}', s)[1]))

def parse(s):
  s = s or ""
  m = re.match(r"(?P<count>\d+)(d(?P<sides>\d+))*(\+(?P<plus>\d+))*", s)
  m2 = re.search(r"(\w+[\s:;.]+)*", s)
  return m2




def Main():
  print handlebars("The cat sat on a box.")
  print temp_slice("alsdfkj")
  print words("The {#green}.cat{# reset }a(sdf sa(t {#green}{#green} on a box{#green}a coin{#green}).")
  print handlebars("{#yellow}wooden sign{#reset}")



if __name__== '__main__' :Main()



