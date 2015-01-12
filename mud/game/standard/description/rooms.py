from mud.core import *
from mud.core.CAPSMODE import *

def center(s):
	return '{:^80}'.format(s)

def paragraph(s, width=80, margin="  ", indent="  "):
	# width = width-len(margin)*2
	# layout = margin+'{:<'+str(width)+'}'
	# res = []
	# s = indent + s
	# for i in range(50):
	# 	line = parse.temp_slice(s, 0, width)
	# 	s = s[len(line):]
	# 	res.append(layout.format(line))
	# 	if not s: break
	# return "\r\n".join(res)

	ind = "  "+s
	sp = parse.words(s)
	final = []
	l = 2
	res = []
	for w in sp:
		wlen = parse.length(w)
		if wlen + l > 74:
			final.append('   {:<74}'.format(" ".join(res)))
			l = wlen+1
			res = [w]
		else:
			l += wlen+1
			res.append(w)
	final.append('   {:<74}'.format(" ".join(res)))
	final[0] = "  "+final[0]
	return "\r\n".join(final)

@before("player", "room")
def describe(p, r):
  say("\r\n{#bold}"+center(call("write",r,'name'))+"{#reset}\r\n ")

def descenic(e): return e["scenery"]

@given("player", "room")
def describe(p, r):
    ps = call("write",r,'desc').split("\r\n")
    conts = contents_of(r)
    scenics = map(util.its("scenery"), filter(a("scenic"), conts))

    say("{#white}{#bold}"+"\r\n\r\n".join(map(paragraph, ps + scenics))+"{#reset}")

    #say("\r\n"+"You see "+ call("list_contents", p, r)+ ".\r\n")
    conts.remove(p)
    call("sort_contents", p, conts)

    say("   exits: {#yellow}{#bold}"+", ".join(the(r, 'exits').keys()) + "{#reset}\r\n")



@given("player", sequential)
def sort_contents(p, r):
  listed = GROUP_BY(has("unlisted"), r)
  enti = GROUP_BY(has("entity"), GET(listed,False, []))
  gend = GROUP_BY(has("gender"), GET(enti,True, []))
  listed = map(INF(call, "list_contents", "%1"), map(INF(GET, "%1", "%2", []), [gend,gend,enti], [True, False, False]))
  res = []
  if GET(listed, 0):
  	res.append(GET(listed, 0)+ " are here.")
  if GET(listed, 1):
  	res.append(GET(listed, 1)+ " here as well.")
  if GET(listed, 2):
  	res.append("On the floor is "+ GET(listed, 2)+ ".")
  say("\r\n"+paragraph(" ".join(res))+"\r\n")






