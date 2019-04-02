#!/usr/bin/env python3

import json
import re

p = re.compile('^"(\d{4}-\d\d-\d\d)-([0-9a-f-]+)" ([0-9.]+)$')

polls = {}

with open ('../../data/abgeordnetenwatch.de.json') as json_data:
    d = json.load(json_data)
    for poll in d["polls"]:
        polls[poll["meta"]["uuid"]] = poll

with open ("variance.table") as v:
  with open ("variance.questions", 'w') as q:
    for line in v:
      m = p.match (line)
      if m:
        q.write ("'" + polls[m.group(2)]["title"] + "'," + m.group(3) + "," + m.group(2) + "," + polls[m.group(2)]["meta"]["url"])
        q.write ("\n")
        #print (polls[m.group(2)])
      else:
        raise Exception('line did not match: ' + line)







