#!/usr/bin/env python
# encoding=utf8

abstimmungs_dir = '..'

import os
import re
import json
import sys
sys.path.append (abstimmungs_dir)
from abstimmungsparser import Abstimmung

schwaenzer = {}

for subdir, dirs, files in os.walk (abstimmungs_dir):
	for directory in dirs:
		# abtimmungsverzeichnisse starten alle mit "018-"
		if "018-" in directory:
			# die abstimmungsdaten sind im file "index.md"
			abstimmungs_file = os.path.join (subdir, directory, "index.md")
			if os.path.isfile (abstimmungs_file):
				# abstimmung parsen und den titel ausgeben
				abstimmung = Abstimmung ()
				abstimmung.parse_abstimmung (abstimmungs_file)
				
				ergebnis = abstimmung.get_abstimmungs_ergebnisse ()
				
				for party in ergebnis:
					if "file" in party:
						continue
					if not party in schwaenzer:
						schwaenzer[party] = {
							'absolut': 0,
							'relativ': 0.0,
							'abstimmungen': 0
							}
					
					schwaenzer[party]['absolut'] += ergebnis[party]['nichtabgegeben']
					schwaenzer[party]['relativ'] += float (ergebnis[party]['nichtabgegeben']) / float (ergebnis[party]['gesamt'])
					schwaenzer[party]['abstimmungen'] += 1
					

print json.dumps (schwaenzer, indent=4, separators=(',', ': '))
