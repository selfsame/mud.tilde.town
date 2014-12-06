sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import parse

def partial(s1, s2):
  if s1.lower() == s2[:len(s1)].lower()
    return True
  return False


def guess(actor, s):
  room = actor.room()
  exits = room['exits']
  for e in exits:
    if partial(s, e):
      print "exit"
      




