import json, os, sys
import uuid
from CAPSMODE import *
from mud.core import components 
from mud.core import dispatch



datatypes = {}
instances = {}
game = {}

relations = {}
associations = {}


def get_uuid(s):
  if isinstance(s, str):
    r = data.instances.get(s)
    if r: return r
  elif isinstance(s, dict):
    r = GET(s, "uuid")
    if r: return r
  print "NO get_uuid FOR ", s

def associate(relation, a, b):
    a = get_uuid(a)
    b = get_uuid(b)
    if not GET(associations, relation): associations[relation] = {}
    if not GET(associations[relation], a): associations[relation][a] = []
    associations[relation][a].append(b)

def related(a, relation, b):
    a = get_uuid(a)
    b = get_uuid(b)
    rel = GET(associations, relation)
    if rel:
        if GET(associations[relation], a):
            if b in GET(associations[relation], a):
                return True
    return False


def u_to_str(v):
	if isinstance(v, unicode):
		return str(v)
	return v

def decode_strings(ob):
  res = {}
  for k in ob:
    v = ob[k]
    if isinstance(k, unicode):
      k = str(k)
    if isinstance(v, unicode):
      v = str(v)
    if isinstance(v, list):
      v = map(u_to_str, v)
    res[k] = v
  return res

def load_json(path):
    file = open(path)
    try:
        fstr = file.read()
        res = json.loads(fstr, encoding="utf-8", object_hook=decode_strings)
        file.close()
        return res
    except:
        file.close()
        print path, fstr
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
    print "loading... "
    for subdir, dirs, files in os.walk(pathname):
        files.sort()
        for file in files:
            mime = file.split(".")[-1]
            if mime == "json":
                fpath = subdir + os.sep + file
                print fpath
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
                        #data["base"] = True
                    
                    # find bases by iterating the paths
                    sp = subdir.split(os.sep)
                    found_bases = []
                    for i in range(len(sp)):
                        kp = os.sep.join(sp[0:i+1])
                        if kp in bases:
                            found_bases.append(bases[kp])

                    # merge base types
                    dtbases = found_bases
                    if is_base: dtbases = found_bases[:-1]
                    
                    dts = map(lambda x: datatypes[x], dtbases)
                    print "["+">".join(map(KEYFN("id"), dts + [data]))+"]"
                    merged = components._merge(dts + [data])
                        
                    datatypes[ustr] = merged

                    



def instance(ustr, reg=True):
    nuuid = uuid.uuid1().hex
    result = {}
    if ustr in datatypes:
        template = datatypes[ustr]
        res = components._construct(template)
        res["uuid"] = ustr+nuuid
        if "extends" in res:
            dts = map(lambda x: datatypes[x], res["extends"])
            merged = components._merge(dts + [res])
            if reg:
                result = register(merged)
            else:
                result = merged
        else:
            if reg:
                result = register(res)
            else: 
                result = res
    if reg:
        dispatch.stack("init", result)
    return result


def register(thing):
    if "uuid" in thing:
        uid = thing["uuid"]
        instances[uid] = thing
    dispatch.call("register", thing)
    return thing


def delete(thing):
    if not thing or thing == None: return
    if not isinstance(thing, dict): return
    if "uuid" in thing:
        uid = thing["uuid"]
        if uid in instances:
            del instances[uid]
    