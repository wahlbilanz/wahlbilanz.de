#!/usr/bin/env python3

abstimmungs_dir = '..'
import os
import re
import json
import sys
from os import listdir
from os.path import isfile, join
sys.path.append (abstimmungs_dir)
from abstimmungsparser import Abstimmung
import pandas as pd

pages = []
parties = [
"AfD",
"Bündnis 90/Die Grünen",
"Die Linke",
"FDP",
"cdu/csu",
"fraktionslos",
"spd",
]


for f in listdir (abstimmungs_dir):
  d = os.path.join (abstimmungs_dir, f)
  if os.path.isdir (d) and f.startswith('019'):
    abstimmungs_file = os.path.join (d, "index.md")
    if os.path.isfile (abstimmungs_file):
      # abstimmung parsen und den titel ausgeben
      abstimmung = Abstimmung ()
      abstimmung.parse_abstimmung (abstimmungs_file)
      abst_key = "%03d-%02d" % (abstimmung.get_bundestagssitzung(), abstimmung.get_abstimmung())
      p = [
        abstimmung.get_bundestagssitzung(),
        abstimmung.get_abstimmung(),
        abstimmung.get_datum(),
        abstimmung.get_title().replace ("Abstimmung: ", ""),
        "https://wahlbilanz.de/abstimmungen/019-" + abst_key
      ]
      ergebnisse = abstimmung.get_abstimmungs_ergebnisse ()
      print (ergebnisse)
      for party in parties:
        p.append((ergebnisse[party]['ja'] - ergebnisse[party]['nein']) / ergebnisse[party]['gesamt'])
      
      
      pages.append(p)
      # if (len (pages) > 5):
        # break


cols = ["Sitzung", "Abstimmung", "Datum", "Titel", "Link"]
for party in parties:
  cols.append (party)

df = pd.DataFrame(pages, columns = cols)

df.to_csv ('/tmp/uebersicht.csv', index=False)

# print (pages)

# for key, value in sorted(pages.items(), key=lambda x: x[0], reverse=True):
  # print (value)
  
