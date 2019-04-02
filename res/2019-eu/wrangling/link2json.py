#!/usr/bin/env python3

import json
import sys

if len(sys.argv) != 2 or sys.argv[1] == "-h" or sys.argv[1] == "--help":
  print ("submit an link to a EU poll on abgeordnetenwatch.de as an argument to obtain the coresponding json snippet")
  print ("eg:")
  print ("    python3 link2json.py https://www.abgeordnetenwatch.de/eu-parlament-2014-2019/abstimmungen/freihandelsabkommen-mit-singapur")
  sys.exit (1)

url = sys.argv[1]
found = False

with open ('../data/abgeordnetenwatch.de.json') as json_data:
    d = json.load(json_data)
    for poll in d["polls"]:
        if url == poll["meta"]["url"]:
          print (json.dumps(poll, indent=4, sort_keys=True))
          found = True

if not found:
  print ("did not find this URL")
