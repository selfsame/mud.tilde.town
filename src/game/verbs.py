import re
verbs = {"l$|look$":"look",
        "go$|enter$|leave$|walk$":"walk",
        "get$|take$|grab$":"take",
        "drop$|discard$":"drop",
        "inv$|i$|inventory$":"inventory",
        "quit$":"quit",
        "save$":"save",
        "say$|^'":"talk",
        "who$":"who"}


regexverbs = {"^(\W*look at|look|l|examine|x)\W*(.*)":"look",
			 "^(\W*get|take|grab|pick up)\W+(.*)":"take",
			 "^(\W*drop|put|place|set|throw)\W+(.*)":"drop",
			 "^(\W*give|hand)\W+(.*)":"give",
			 "^(\W*close|shut)\W+(.*)":"close",
			 "^(\W*open|unlock)\W+(.*)":"open",
			 "^(\W*go|enter|leave|walk)\W+(.*)":"walk",
			 "^(\W*quit)\W*(.*)":"quit",
			 "^(\W*save)\W*(.*)":"save",
			 "^(\W*inventory|inv|i)\W*(.*)":"inventory"}

compiled = {}

for regex in regexverbs:
	val = regexverbs[regex]
	compiled[re.compile(regex)] = val



numeric = re.compile("\W(second|third|fourth|fifth|sixth|seventh|eight)\W")
predicate = re.compile("\W(open|closed|locked|unlocked)\W")
article = re.compile("(\W+|^)(a|an|the)\W+")
adverb = re.compile("\W(with|using|to|for)\W")


inside = re.compile("\W+from\W+inside|\W+from\W+in\W|\W+inside\W+of?|\W+inside|\Winto?|\Win\W")

v_s = re.compile("{VERB}\W*{A}?\W*(?P<subject>[^{]+)$")
gruper = re.compile("{VERB}\W*{A}?\W*(?P<subject>[^{]+)\W*((?P<s_holder>{IN}?\W*{A}?)|(?P<s_adverb>{ADVERB}?\W*{A}?))(?P<predicate>[^{]+)?")
splitter = re.compile("{[A-Z]+}")


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
			print rest
			holded = inside.split(rest)
			
			if len(holded) > 1:
				subject = holded[0]
				predicate = holded[1]
				if verb == "drop": return [verb, ["noun", subject.strip()], ["noun", predicate.strip()]]
				else: return [verb, ["container", predicate.strip()], ["noun", subject.strip()]]
			else:
				return [verb, ["noun", holded[0].strip()]]
	return []



def comprehend(s):
	subbed = adverb.sub(" {ADVERB} ", article.sub(" {A} ",  inside.sub("{IN} ", s)))
	verb = False
	for k in compiled:
		v = compiled[k]
		m = k.search(subbed)
		if m:
			verb = v
			verbed = k.sub("{VERB}", subbed)
			chopped = splitter.split(verbed)
			grupped = gruper.search(verbed)
			#print verbed, chopped
			print s
			if grupped: 
				gd = grupped.groupdict()
				if gd:
					#print gd
					if gd["s_holder"]:
						return [verb, ["container", [gd["predicate"]]], ["noun", gd["subject"]]]
					elif gd["s_adverb"]:
						return [verb, ["noun", gd["subject"]], ["noun", gd["predicate"]]]
					else:
						return [verb, ["noun", gd["subject"]], ["noun", gd["predicate"]]]
					break
			else:
				vs = v_s.search(verbed)
				if vs: 
					return [verb, ["noun", vs.groupdict()["subject"]]]

					


tests = ["look", "look at coin in the box", "take the lamp inside of the box", "look at the first locker inside the boat",
		"put the second coin inside of the third cup"]
#"close the cabinet inside of the coach.", 
#"unlock the first locker with the second key", "put the coin inside the bag", "say haha say hell man. this is great!"]
#print map(determine, tests)

