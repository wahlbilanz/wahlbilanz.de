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

pages = {}

for f in listdir (abstimmungs_dir):
  d = os.path.join (abstimmungs_dir, f)
  if os.path.isdir (d) and "-" in f and f[0] == '0':
    abstimmungs_file = os.path.join (d, "index.md")
    if os.path.isfile (abstimmungs_file):
      # abstimmung parsen und den titel ausgeben
      abstimmung = Abstimmung ()
      abstimmung.parse_abstimmung (abstimmungs_file)
      pages[f] =  ('* [' + abstimmung.get_title().replace ("Abstimmung: ", "") + ']('+f+'/) ('+str(abstimmung.get_bundestagssitzung())+'. Sitzung des '+str(abstimmung.get_legislaturperiode())+'. Deutschen Bundestages '+abstimmung.get_datum()+')')


for key, value in sorted(pages.items(), key=lambda x: x[0], reverse=True):
  print (value)
  
