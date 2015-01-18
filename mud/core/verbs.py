import re

__all__ = ['determine', 'register', 'register_structure', 'forms', 'structures']

regexverbs = {}
compiled = {}
forms = {}
structures = {}

def register_structure(v, *patterns):
  if v not in structures:
    structures[v] = []
  group = structures[v]
  for pattern in patterns:
    if pattern not in group:
      structures[v] = [pattern] + group

def register(name, regex, tenses = {}):
  command_pattern = "^(\W*"+regex+")\W*(.*)"
  c = re.compile(command_pattern)
  compiled[c] = name
  default = {"present":name+"s",
         "past":name+"ed",
         "progressive":name+"ing"}
  forms[name] = dict(tenses.items() + default.items())
  register_structure(name, "{1}")

for regex in regexverbs:
  name = regexverbs[regex]
  register(name, regex)


numeric = re.compile("\W(second|third|fourth|fifth|sixth|seventh|eight)\W")
article = re.compile("(\W+|^)(a|an|the)\W+")
adverb = re.compile("\W(with|using|to|for)\W")


inside = re.compile("\W+from\W+inside|\W+from\W+in\W|\W+inside\W+of?|\W+inside|\Winto?|\Win\W")
on = re.compile("\W+on|on top of\W")

token = re.compile("(\{[0-9]+\:?[a-z]*\}|[^\{]+)")
handle = re.compile("\{([0-9]+)\:?([a-z]*)\}")

def match_pattern(p, s):
  #checks structures[verb] for patterns and returns first match
  parts = re.findall(token, p)
  res = []
  types = {}
  for p in parts:
    if handle.search(p):
      tk = handle.search(p).groups()
      res.append("(?P<g"+tk[0]+">.+)")
      if tk[1]:
        types["g"+tk[0]] = tk[1]
      else:
        types["g"+tk[0]] ="noun"
    else:
      res.append("("+p+")")
  res = "".join(res)
  fpat = re.compile( "".join(res) )
  r = re.match(fpat, s)
  if r: 
    gd = r.groupdict()
    res = []
    if "g1" in gd:
      res.append({types["g1"]: gd["g1"]})
    if "g2" in gd:
      res.append({types["g2"]: gd["g2"]})
    if "g3" in gd:
      res.append({types["g3"]: gd["g3"]})
    if "g4" in gd:
      res.append({types["g4"]: gd["g4"]})
    if "g5" in gd:
      res.append({types["g5"]: gd["g5"]})
    return res
  else:
    return False

def tokenize_noun(s):
  s = article.sub(" ", s)
  held = inside.split(s)
  if len(held) > 1:
    return {"string":held[0].strip(),
        "holder":tokenize_noun(" inside ".join(held[1:]))}
  return {"string":s.strip()}

def determine(s):
  for k in compiled:
    verb = compiled[k]
    r = k.search(s)
    if r:
      rest = r.groups()[1]
      if rest == "":
        return [verb]
      patterns = structures[verb]
      if patterns:
        for p in patterns:
          tokenized = match_pattern(p,rest)
          if tokenized:
            res = [verb]
            for t in tokenized:

              if "noun" in t:
                t["noun"] = tokenize_noun(t["noun"])
              res.append(t)
            return res
      return [verb]
  return []



def Main():
  tests = ["drop the coin inside the boat in the ocean",
      "put the second coin inside of the third cup"]
  print map(determine, tests)



if __name__== '__main__' :Main()

