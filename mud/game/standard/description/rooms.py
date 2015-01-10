from mud.core import *


def center(s):
	return '{:^80}'.format(s)

def paragraph(s):
	ind = "  "+s
	sp = ind.split()
	final = []
	l = 2
	res = []
	for w in sp:
		if len(w) + l > 74:
			final.append('   {:<74}'.format(" ".join(res)))
			l = len(w)+1
			res = [w]
		else:
			l += len(w)+1
			res.append(w)
	final.append('   {:<74}'.format(" ".join(res)))
	final[0] = "  "+final[0]
	return "\r\n".join(final)

@before
@given("player", "room")
def describe(p, r):
  say("\r\n{#bold}"+center(act("write",r,'name'))+"{#reset}\r\n ")

def descenic(e):
	return e["scenery"]

@action
@given("player", "room")
def describe(p, r):
    ps = act("write",r,'desc').split("\r\n")
    conts = contents_of(r)
    scenics = map(util.its("scenery"), filter(a("scenic"), conts))

    say("\r\n\r\n".join(map(paragraph, ps + scenics)))

    say("\r\n"+"You see "+ act("list_contents", p, r)+ ".\r\n")
    say("exits: {#yellow}{#bold}"+", ".join(the(r, 'exits').keys()) + "{#reset}\r\n")













