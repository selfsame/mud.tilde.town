import re

__all__ = ['determine', 'register', 'forms']

regexverbs = {"look at|look|l|examine|x":"look",
			 "get|take|grab|pick up":"take",
			 "drop|put|place|set|throw":"drop",
			 "give|hand":"give",
			 "close|shut":"close",
			 "open|unlock":"open",
			 "go|enter|leave|walk":"walk",
			 "quit":"quit",
			 "save":"save",
			 "inventory|inv|i":"inventory"}

compiled = {}
forms = {}

def register(name, regex, tenses = {}):
	command_pattern = "^(\W*"+regex+")\W*(.*)"
	c = re.compile(command_pattern)
	compiled[c] = name
	default = {"present":name+"s",
			   "past":name+"ed",
			   "progressive":name+"ing"}
	forms[name] = dict(tenses.items() + default.items())

for regex in regexverbs:
	name = regexverbs[regex]
	register(name, regex)



numeric = re.compile("\W(second|third|fourth|fifth|sixth|seventh|eight)\W")
predicate = re.compile("\W(open|closed|locked|unlocked)\W")
article = re.compile("(\W+|^)(a|an|the)\W+")
adverb = re.compile("\W(with|using|to|for)\W")


inside = re.compile("\W+from\W+inside|\W+from\W+in\W|\W+inside\W+of?|\W+inside|\Winto?|\Win\W")




def determine(s):
	speak = re.compile("^\W*(say\W+|[\'])(?P<string>.*)")
	a = speak.search(s)
	if a:
		return ["talk", ["arg", a.groupdict()["string"]]]
	for k in compiled:
		verb = compiled[k]
		r = k.search(s)
		if r:
			groups = r.groups()
			rest = groups[1]
			if rest == "":
				return [verb]
			rest = article.sub(" ", rest)
			holded = inside.split(rest)
			
			if len(holded) > 1:
				subject = holded[0]
				predicate = holded[1]
				if verb == "drop": return [verb, ["noun", subject.strip()], ["noun", predicate.strip()]]
				else: return [verb, ["container", predicate.strip()], ["noun", subject.strip()]]
			else:
				return [verb, ["noun", holded[0].strip()]]
	return []

			





def Main():
 	tests = ["look", "look at coin in the box", "take the lamp inside of the box", "look at the first locker inside the boat",
			"put the second coin inside of the third cup"]
	print map(determine, tests)

if __name__== '__main__' :Main()

