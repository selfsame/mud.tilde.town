import os, sys
import json
import uuid
from data import *
import components

def load_json_comp(path):
    file = open(path)
    try:
        fstr = file.read()
        res = json.loads(fstr)
        file.close()
        return res
    except:
        file.close()
        raise

def compstruct(d):
    res = {}
    for k in d:
        comp = components.construct(k, d[k])
        res[k] = comp
    return res


def load(path):
    bases = {}
    pathname = os.path.dirname(sys.argv[0]) + path
    for subdir, dirs, files in os.walk(pathname):
        for file in files:
            mime = file.split(".")[-1]
            if mime == "json":
                fpath = subdir + "/" + file
                print "loading " + fpath + "..."
                data = load_json_comp(fpath)
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
                    
                    # find bases by iterating the paths
                    sp = subdir.split("/")
                    found_bases = []
                    for i in range(len(sp)):
                        kp = "/".join(sp[0:i+1])
                        if kp in bases:
                            found_bases.append(bases[kp])
                    # if base data in the path, add the last base to 
                    # the extends comp (but if I am a base we have to find the
                    # previous
                    bl = 1 if is_base else 0
                    bi = -2 if is_base else -1
                    if len(found_bases) > bl:
                        ex = data.get("extends") or []
                        data["extends"] = [found_bases[bi]] + ex
                    datatypes[ustr] = data

def instance(ustr):
    nuuid = uuid.uuid1().hex
    if ustr in datatypes:
        template = datatypes[ustr]
        res = compstruct(template)
        res["uuid"] = nuuid
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
            rooms[uid] = thing
        if "object" in thing:
            objects[uid] = thing
        if "entity" in thing:
            entities[uid] = thing

def delete(thing):
    if "uuid" in thing:
        uid = thing["uuid"]
        if uid in instances:
            del instances[uid]
        if uid in rooms:
            del rooms[uid]
        if uid in objects:
            del objects[uid]
        if uid in entities:
            del entities[uid]


