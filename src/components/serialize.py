
"""
component functions to transform their data for json serialization. (probably)
"""

def _symbol(s):
  try:
    return globals()[s]
  except:
    return False

def living(d):
  return {"hp": d["hp"]}
