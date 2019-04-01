#!/usr/bin/env python3

import json


parties = {}
polls = []
out = "summary.table"




def translate_party (x):
  x = x.lower ()
  if "afd" in x and "efdd" in x:
    return "AfD_EFFD"
  if "alfa" in x and "familie" in x and "ekr" in x:
    return "ALFA_FAMILIEN.PARTEI_EKR"
  if "afd" in x and "enf" in x:
    return "AfD_ENF"
  if "cdu" in x and "evp" in x and "csu" in x:
    return "CDU_CSU_EVP"
  if "die gr" in x and "piraten" in x and "efa" in x:
    return "GRUENE_PIRATEN_ODP_EFA"
  if "die linke" in x and "gue" in x and "ngl" in x:
    return "LINKE_GUE_NGL"
  if "fdp" in x and "freie w" in x and "alde" in x:
    return "FDP_FREIE.WAEHLER_ALDE"
  if "gue/ngl" == x:
    return "GUE_NGL"
  if "spd" in x and "s&d" in x:
    return "SPD_S.D"
  if "fraktionslos" in x:
    return "fraktionslos"
  raise Exception('unkown party key: ' + x)

def translate_vote (x):
  if x.startswith ("daf"):
    return "dafuer"
  if x.startswith ("dag"):
    return "dagegen"
  if x.startswith ("enth"):
    return "enthalten"
  if x.startswith ("nicht"):
    return "abwesend"
  raise Exception('unkown vote key: ' + x)

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



with open ('../data/abgeordnetenwatch.de.json') as json_data:
    d = json.load(json_data)
    for poll in d["polls"]:
        pid = poll["date"] + "-" + poll["meta"]["uuid"]
        polls.append (pid)
        for party in poll["stats"]:
          if party == "total":
            continue
          party_norm = translate_party (party)
          if party_norm not in parties:
            parties[party_norm] = {}
          parties[party_norm][pid] = {
              "dafuer": 0,
              "dagegen": 0,
              "enthalten": 0,
              "abwesend": 0
              }
          for vote in poll["stats"][party]:
            parties[party_norm][pid][translate_vote(vote)] = poll["stats"][party][vote]

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



