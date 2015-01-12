from mud.core import *
from mud.core.CAPSMODE import *

bind.predicate("Dialogue", INF(isinstance,"%1", Dialogue))

def _dialogued(e):
  try: 
    if e["player"].dialogue: return True
  except: return False

bind.predicate("dialogued", _dialogued)

@given("MUDClient", "Dialogue")
def end_dialogue(d, c):
  d.clear()
  call("player_input", d.player, "look")