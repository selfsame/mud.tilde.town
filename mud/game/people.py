from mud.core import *
from mud.core.util import *
import random
from mud.core.CAPSMODE import *

@construct
def traits(d):
	return {
	"height":random.randint(54,74),
	"haircolor":random.choice(["black","brown","red","blonde"]),
	"age":random.randint(2,112)}

@construct
def gender(d): return random.choice(["m","f"])

_gt = {"m":"man","f":"woman", "o":"person"}

def _male(e): return GET(e,"gender") == "m"
def _female(e): return GET(e,"gender") == "f"
def _nonbinary(e): return GET(e,"gender") == "o"

def _adult(e): return GET(GET(e,"traits"),"age") > 14

bind.predicate("person", a(has("gender"),has("traits")))
bind.predicate("male", _male)
bind.predicate("female", _female)
bind.predicate("nonbinary", _nonbinary)
bind.predicate("adult", a(_adult, "person"))
bind.predicate("child", a(non(_adult), "person"))

bind.adjective("male", "male")
bind.adjective("female", "female")
bind.adjective("adult", "adult")

@given("person")
def adjectives(e):
  return e["traits"]["haircolor"]+" haired"

@given("person", "player")
def print_name_for(e, o):
  if data.related(o, "knows", e):
    noun = GET(e,"firstname","?") + " " + GET(e,"lastname","?")
    return noun
  adjectives = ", ".join(stack("adjectives", e))
  noun = str(GET(GET(e, "kind"), -1, "thing|things").split("|")[0])
  if adjectives:
    noun = adjectives+" "+noun
  return str(call("indefinate_article", noun)+noun)


@given("female")
def plural_name(e): return "women"

@given("male")
def plural_name(e): return "men"

@given("nonbinary")
def plural_name(e): return "people"

@given("person")
def init(e):
  if not GET(e, "lastname"):
  	e["lastname"] = random.choice([
  	"Homayoun", "Hooshang", "Mazandarani", "Mokri", "Mohsen", "Ebrahimi", "Esfahani", "Martinez", 
  	"Juan", "Ruiz", "Garcias", "Venediktov", "Dezhnyov", "Kozlovsky", "Alemseged", "Asfaw", "Dibaba", "Kibebe"])

@given(a("female", "person"))
def init(e):
  if not GET(e, "firstname"):
    e["firstname"] = random.choice([
      "Anousheh", "Arezu", "Arian", "Mahshid", "Maryam", "Mehregan", "Mina", "Mithra", "Anita", "Marcela", 
      "Estefania", "Maria", "Sasha", "Katrina", "Anya", "Mashenyka", "Frehiwot", "Dershaye", "Eyerusalem", "Geni"])

@given(a("male", "person"))
def init(e):
  if not GET(e, "firstname"):
    e["firstname"] = random.choice([
      "Mahmoud", "Mazdak", "Mazdan", "Maziar", "Sassan", "Sepehr", "Ardashir", "Aria", "Vladimir", "Alexander", 
      "Constantine", "Yorgi", "Olaf", "Yonatan", "Ermiyas", "Sintayehu", "Abiy", "Narantsetseg", "Enkhtuyaa", "Nergui"])

bind.kind("woman|women")
bind.kind("man|men")
bind.kind("girl|girls")
bind.kind("boy|boys")
bind.kind("child|children")
bind.kind("person|people")

@given(a("adult", "nonbinary"))
def init(e):
	e["kind"].append("person|people")

@given(a("adult", "female"))
def init(e):
	e["kind"].append("woman|women")

@given(a("adult", "male"))
def init(e):
	e["kind"].append("man|men")

@given(a("female", "child"))
def init(e):
	e["kind"].append("girl|girls")

@given(a("male", "child"))
def init(e):
	e["kind"].append("boy|boys")

@given("child")
def init(e):
	e["kind"].append("child|children")

@given("entity", "player")
def print_reflexive_for(e, o):
  return "itself"

@given("nonbinary", "player")
def print_reflexive_for(e, o):
  return "themself"

@given("male", "player")
def print_reflexive_for(e, o):
  return "himself"

@given("female", "player")
def print_reflexive_for(e, o):
  return "herself"



bind.predicate("sentient", has("sentient"))

bind.verb("introduce", "introduce", {"doc":"Attempt to indtroduce yourself to a stranger, or introduce two people you know to each other."})
bind.verb_pattern("introduce", "{1}","{1}to{2}")

@check("player", "entity")
def introduce(a, b):
  if a == b:
  	say("You would feel silly introducing you to yourself.")
  if data.related(b, "knows", a):
  	say("They have allready been introduced to you.")
  	return False
  return True

@given("player", "entity")
def introduce(a, b):
  report("[Subject] introduce[s] [itself] to [object].")
  call("was_introduced", a, b)
  call("was_introduced", b, a)

@given("entity", "entity")
def was_introduced(a, b):
  message = "nice to meet you, my name is "+GET(a,"firstname","?")+" "+GET(a,"lastname","?")
  call("tell", a, b, message)
  understood.previous()
  data.associate("knows", b, a)


@given("player", "entity", "entity")
def introduce(a, b, c):
  pass