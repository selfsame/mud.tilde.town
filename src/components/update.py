
"""
  component functions for delta updates, 
  arg1: the owning entity dict
  arg2: the delta time since last update call

  they are not expected to return a value
"""

def _symbol(s):
  try:
    return globals()[s]
  except:
    return False

def living(this, delta):
  print "updating " + str(this)
