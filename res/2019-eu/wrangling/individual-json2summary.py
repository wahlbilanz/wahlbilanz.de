#!/usr/bin/env python3

import json


parties = {}
polls = []
out = "summary-from-individuals.table"





def calc_ratio (vote):
  ja = 0.0
  nein = 0.0
  if "dafuer" in  vote:
    ja = float(vote["dafuer"])
  if "dagegen" in vote:
    nein = float(vote["dagegen"])
  if ja + nein < 1:
    return -1
  return ja / (ja + nein)



with open ('../data/aggregated-parties.json') as json_data:
    d = json.load(json_data)
    for pid in d:
        polls.append (pid)
        for party in d[pid]:
          #print (party)
          if party not in parties:
            parties[party] = {}
          parties[party][pid] = d[pid][party]


with open (out, 'w') as f:
  f.write ("poll")
  p = []
  for party in parties:
    p.append (party)
    f.write ("\t'" + party + "'")
  f.write ("\n")
  for poll in polls:
    f.write (poll)
    for party in p:
      #print (poll + "  " + party)
      if poll not in parties[party]:
        print ("pid not in party?:" + poll + "  " + party)
        f.write ("\t-1")
      else:
        f.write ("\t" + str (calc_ratio (parties[party][poll])))
    f.write ("\n")



