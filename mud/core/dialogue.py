
class Dialogue:
  def __init__(self, con):
    #we init with a pointer to the chatprotocol connection
    self.con = con
    #this will get overridden with the first dialogue state
    self.state = self.start
    #this is checked to end the dialogue (also can return False from a state)
    self.done = False

  def initial(self):
    return "dialogue begun.."

  def input(self, s):
    return self.state(s)

  def start(self, s):
    return False


