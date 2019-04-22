#!/usr/bin/env python3

import json
import sys
import argparse

parser = argparse.ArgumentParser(description='extract a number of UUIDs of EU votes to the result format for DeinWal.')
parser.add_argument('uuids', type=str, nargs='+',
                    help='uuids to extract')
parser.add_argument('--out', '-o', help='where to store the results?')
args = parser.parse_args()

print (args.out)
print (args.uuids)


found = [False] * len (args.uuids)



results = {}

with open ('../data/aggregated-parties.json') as json_data:
    d = json.load(json_data)
    for poll in d.keys ():
        try:
          i = args.uuids.index (poll)
          if i >= 0:
            found[i] = True
            results[poll] = d[poll]
        except Exception:
          print (poll + " not found")


with open (args.out, 'w') as out:
  out.write (json.dumps (results, indent=4))


print (results)

for i in range (0, len (found)):
  if not found[i]:
    print ("did not find " + args.uuids[i])
