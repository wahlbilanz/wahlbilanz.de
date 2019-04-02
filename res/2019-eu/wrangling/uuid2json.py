#!/usr/bin/env python3

import json
import sys

if len(sys.argv) != 2 or sys.argv[1] == "-h" or sys.argv[1] == "--help":
  print ("submit a UUID of a poll as an argument to obtain the coresponding json snippet (could also be a partial uuid)")
  print ("eg:")
  print ("    python3 ./uuid2json.py 911f414b")
  sys.exit (1)

uuid = sys.argv[1]
found = False

with open ('../data/abgeordnetenwatch.de.json') as json_data:
    d = json.load(json_data)
    for poll in d["polls"]:
        if uuid in poll["meta"]["uuid"]:
          print (json.dumps(poll, indent=4, sort_keys=True))
          found = True

if not found:
  print ("did not find this UUID")
