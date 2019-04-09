#!/usr/bin/env python3

import json
import os

def translate_party (x):
  x = x.lower ()
  if "afd" in x:
    return "AFD"
  if "cdu" in x or "csu" in x:
    return "CDU/CSU"
  if "die gr" in x:
    return "GRUENE"
  if "linke" in x:
    return "LINKE"
  if "fdp" in x:
    return "FDP"
  if "spd" in x:
    return "SPD"
  if "liberal-konservative" in x:
    return "ALFA"
  if "blaue" in x:
    return "BLAUE"
  if "piraten" in  x:
    return "PIRATEN"
  if "die partei" in x:
    return "DIEPARTEI"
  if "ndnis c" in x:
    return "BUENDNISC"
  if "freie w" in x:
    return "FREIEWAEHLER"
  if "dp" in x and len(x) == 3:
    return "OEDP"
  if "npd" in x:
    return "NPD"
  if "fraktionslos" in x or "parteilos" in x:
    return "individual"
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


parties = {}
voteids = []
sd = "abgeordnetenwatch-individual-votes/"

for filename in os.listdir(sd):
    if "json" not in filename:
        continue
    with open(sd + filename) as json_data:
        d = json.load(json_data)
        username = d["profile"]["meta"]["username"]
	#print (username)
        party =  translate_party (d["profile"]["party"])
	if party not in parties:
		parties[party] = {}
        #print (party)
	for vote in d["profile"]["votes"]:
		if vote["uuid"] not in parties[party]:
			parties[party][vote["uuid"]] = {
				"dafuer": [],
				"dagegen": [],
				"enthalten": [],
				"abwesend": []
				}
			# TODO: check the array length matches number of people
                if vote["uuid"] not in voteids:
                    voteids.append (vote["uuid"])
		parties[party][vote["uuid"]][translate_vote(vote["vote"])].append (username)


partysize = {}

votes = {}

for vid in voteids:
    votes[vid] = {}
    gesamt = 0
    for party in parties:
        votes[vid][party] = {}
        votes[vid][party]["gesamt"] = 0
        for i in parties[party][vid]:
            votes[vid][party][i] = len (parties[party][vid][i])
            votes[vid][party]["gesamt"] += votes[vid][party][i]
        if party not in partysize:
            partysize[party] = votes[vid][party]["gesamt"]
        else:
            if partysize[party] != votes[vid][party]["gesamt"]:
                print ("ohoh!! " + party + " @ " + vid + " is " + str (votes[vid][party]["gesamt"]) + " statt " + str (partysize[party]))
        gesamt += votes[vid][party]["gesamt"]
    if gesamt != 96:
        print (vid)
    print (gesamt)


with open('aggregated-individuals.json', 'w') as outfile:
    json.dump(parties, outfile, indent=2)

with open('aggregated-parties.json', 'w') as outfile:
    json.dump(votes, outfile, indent=2)

