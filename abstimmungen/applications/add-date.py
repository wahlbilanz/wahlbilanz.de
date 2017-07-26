#!/usr/bin/env python
# encoding=utf8

abstimmungs_dir = '..'

import os
import re
import sys
sys.path.append (abstimmungs_dir)
from abstimmungsparser import Abstimmung


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
				preview = abstimmung.get_preview ()
				
				# search for a date in the preview
				if preview:
					m = re.search('am\s*\S+,\s*([0-9]{1,2}.)\s*(\S*)\s*(201[0-9])', preview)
					if (m):
						# found a date -> explicitely set it
						abstimmung.set_datum (m.group(1) + " " + m.group(2) + " " + m.group(3))
						abstimmung.write_abstimmung (abstimmungs_file)
					else:
						# did not find a date!?
						print "did not find date for " + abstimmung.get_title () + " (" + abstimmungs_file + ")"
