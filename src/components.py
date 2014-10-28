#!/usr/bin/env python

def string_to_comp(s):
  try:
    return globals()[s]
  except:
    return False

class C():
    def __init__(self, data):
      self.data = data

    def update(self, delta):
      pass

class visible(C):
  def describe(self):
    print self.data['desc']

class named(C):
  def plural(self):
    self.data['name'] + self.data['plural']

def Main():
  parsed =  {"named":{'name':'mouse', 'plural':'mice'},
           "visible":{"desc":"a visible thing"}}
  print parsed
  res = {}
  for key in parsed:
    cl = string_to_comp(key)
    if cl:
      c = cl(parsed[key])
      res[key] = c
  print res
  
if __name__ == "__main__" :Main()




