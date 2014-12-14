import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))
import json
import uuid
from data import *
import components


def decode_strings(ob):
  res = {}
  for k in ob:
    v = ob[k]
    if isinstance(k, unicode):
      k = str(k)
    if isinstance(v, unicode):
      v = str(v)
    res[k] = v
  return res

def load_json(path):
    file = open(path)
    try:
        fstr = file.read()
        res = json.loads(fstr, object_hook=decode_strings)
        file.close()
        return res
    except:
        file.close()
        raise

def save_json(data, path):
  with open(path, 'w') as f:
    try:
      j = json.dump(data, f, encoding="utf-8")
      return True
    except:
      return False





def load(path):
    bases = {}
    pathname = os.path.dirname(sys.argv[0]) + path
    for subdir, dirs, files in os.walk(pathname):
        files.sort()
        for file in files:
            mime = file.split(".")[-1]
            if mime == "json":
                fpath = subdir + os.sep + file
                print "loading " + fpath + "..."
                data = load_json(fpath)
                if "id" in data:
                    if file == "_base_.json": 
                      is_base = True
                    else: 
                      is_base = False

                    ustr = data["id"]
                    if ustr in datatypes:
                        print "duplicate data for " + ustr
                    if is_base:
                        bases[subdir] = data["id"]
                        data["base"] = True
                    
                    # find bases by iterating the paths
                    sp = subdir.split(os.sep)
                    found_bases = []
                    for i in range(len(sp)):
                        kp = os.sep.join(sp[0:i+1])
                        if kp in bases:
                            found_bases.append(bases[kp])
                    # if base data in the path, add the last base to 
                    # the extends comp (but if I am a base we have to find the
                    # previous
                    bl = 1 if is_base else 0
                    bi = -2 if is_base else -1
                    if len(found_bases) > bl:
                        ex = data.get("extends") or []
                        if "room_base" in found_bases:
                            data["room"] = True
                        data["extends"] = [found_bases[bi]] + ex
                        
                    datatypes[ustr] = data

                    if data.get('room') == True:
                        register(instance(ustr))



def instance(ustr):
    nuuid = uuid.uuid1().hex
    if ustr in datatypes:
        template = datatypes[ustr]
        res = components.construct(template)
        res["uuid"] = ustr+nuuid
        if "extends" in res:
            exres = dict(res["extends"].items() + res.items())
            del exres["extends"]
            return exres
        else:
            return res
    else:
        return {}

def register(thing):
    if "uuid" in thing:
        uid = thing["uuid"]
        instances[uid] = thing
        if "room" in thing:
            #rooms use their id instead of uuid, assumed unique instances
            rooms[thing["id"]] = thing
        if "object" in thing:
            objects[uid] = thing
        if "entity" in thing:
            entities[uid] = thing


def delete(thing):
    if "uuid" in thing:
        uid = thing["uuid"]
        if uid in instances:
            del instances[uid]
        if thing["id"] in rooms:
            del rooms[thing["id"]]
        if uid in objects:
            del objects[uid]
        if uid in entities:
            del entities[uid]
            

