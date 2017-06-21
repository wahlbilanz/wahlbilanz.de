#!/usr/bin/env python
# encoding=utf8



# dieses script hilft neue abstimmungen in die wahlbilanzseite zu integrieren.
# es tut prinzipiell:
# 
# 1. suche nach XLS files die noch nicht konvertiert wurden
# 2. konvertiere nach CSV
# 3. parse CSV und
#   3.1 erstelle dummy page in /abstimmungen
#   3.2 update summary.table
#   3.3 update summary.json


import csv
import os
from os import listdir
from os.path import isfile, join
import sys
import json
import pandas
sys.path.append("../../abstimmungen")
from abstimmungsparser import Abstimmung
import subprocess
import re

abst_dict = {}
rowids = {}
fraktionen = []

summary_json = "summary.json"
summary_table = "summary.table"

wd = os.path.dirname (os.path.realpath(__file__))
xls_path = wd
csv_path = os.path.join (wd, "csv")

xls_to_pdf = re.compile(r"^([0-9]+_[0-9]+)_.*")

# convert to csv, siehe 2. oben
def excel2csv (xls_file, csv_file):
	print "  > converting %s to %s" % (xls_file, csv_file)
	data = pandas.read_excel (xls_file, index_col=None)
	data.to_csv (csv_file, encoding='utf-8', index=False)
	return csv_file


# as they define columnnames and sequence
# arbitarily and everytime differently
# we need to do this effort and match words...
def get_row_ids (header):
	rowids = {
		"periode": 0,
		"siztung": 1,
		"abstimmung": 2,
		"fraktion": 3,
		"ja": 7,
		"nein": 8,
		"enthaltung": 9,
		"ungueltig": 10,
		"nichtabgegeben": 11
		}
	
	for i in range (len (header)):
		columnname = header[i].lower ()
		#print (str (i) + " -> " + columnname)
		if any (option in columnname for option in ["wahlperiode", "periode"]):
			rowids["periode"] = i
			continue
		if any (option in columnname for option in ["sitzungnr", "sitzungnummer", "sitzung"]):
			rowids["siztung"] = i
			continue
		if any (option in columnname for option in ["abstimmnr", "abstimmnummer", "abstimmung"]):
			rowids["abstimmung"] = i
			continue
		if any (option in columnname for option in ["fraktion", "gruppe"]):
			rowids["fraktion"] = i
			continue
		if any (option in columnname for option in ["ja"]):
			rowids["ja"] = i
			continue
		if any (option in columnname for option in ["nein"]):
			rowids["nein"] = i
			continue
		if any (option in columnname for option in ["enthaltung", "enthalten", "enthiel"]):
			rowids["enthaltung"] = i
			continue
		if any (option in columnname for option in ["ungueltig", "ungültig"]) or ("ung" in columnname and "ltig" in columnname):
			rowids["ungueltig"] = i
			continue
		if any (option in columnname for option in ["nichtabgegeben", "nichtabgg"]):
			rowids["nichtabgegeben"] = i
			continue
		
	#print (rowids)
	return rowids


def get_pdf_preview (f):
	return subprocess.check_output (["pdftotext", "-l", "1", f, "-"])




# were there results before?
if os.path.isfile (summary_json):
	with open (summary_json) as data:
		abst_dict = json.load(data)


# siehe 1. oben
for f in listdir (xls_path):
	if not "xls-data.xls" in f:
		continue
	
	xls_file = os.path.join (xls_path, f)
	csv_file = os.path.join (csv_path, f[:-3] + "csv")
	
	if isfile (csv_file):
		# we already processed this file
		#print "- ignoring %s as it is already converted..." % f
		continue
	
	print "> processing %s" % f
	
	# convert to csv, siehe 2. oben
	print "  > converting to CSV"
	excel2csv (xls_file, csv_file)
	
	# parse csv, siehe 3. oben
	print "  > parsing values CSV"
	with open(csv_file, 'rb') as csvfile:
			dialect = csv.Sniffer ().sniff (csvfile.read(1024), delimiters = ";,")
			csvfile.seek (0)
			table = csv.reader (csvfile, dialect)
			
			# go through the table
			for row in table:
				# parse row sequence...
				if "Wahlperiode" in row:
					rowids = get_row_ids (row)
					continue
				
				
				abst_key = "%03d-%03d-%02d" % (int (row[rowids["periode"]]), int (row[rowids["siztung"]]), int (row[rowids["abstimmung"]]))
				fraktion = row[rowids["fraktion"]]
				
				if 'B' in fraktion and 'gr' in fraktion.lower ():
					fraktion = 'Gruenen'
				
				if 'linke' in fraktion.lower ():
					fraktion = 'die.linke'
				
				fraktion = fraktion.lower ()
				
				if fraktion not in fraktionen:
					fraktionen.append (fraktion)
				
				if abst_key not in abst_dict:
					abst_dict[abst_key] = {}
				abst_dict[abst_key]["file"] = f
				
				if fraktion not in abst_dict[abst_key]:
					abst_dict[abst_key][fraktion] = { "ja": 0, "nein": 0, "enthaltung": 0, "ungueltig": 0, "nichtabgegeben": 0, "gesamt": 0 }
				
				abst_dict[abst_key][fraktion]["ja"] += int (row[rowids["ja"]])
				abst_dict[abst_key][fraktion]["nein"] += int (row[rowids["nein"]])
				abst_dict[abst_key][fraktion]["enthaltung"] += int (row[rowids["enthaltung"]])
				abst_dict[abst_key][fraktion]["ungueltig"] += int (row[rowids["ungueltig"]])
				abst_dict[abst_key][fraktion]["nichtabgegeben"] += int (row[rowids["nichtabgegeben"]])
				abst_dict[abst_key][fraktion]["gesamt"] += 1
				
				
			# create new page, see 3.1 oben
			jekyll_file = os.path.abspath (os.path.join (wd, "../../abstimmungen/" + abst_key + "/index.md"))
			if not os.path.isfile (jekyll_file):
				print "  > erstelle neue abstimmungsseite"
				pdf_file = xls_to_pdf.sub ("\\1-data.pdf", f)
				
				abstimmung = Abstimmung ()
				abstimmung.set_abstimmung (int (row[rowids["abstimmung"]]));
				abstimmung.set_bundestagssitzung (int (row[rowids["siztung"]]));
				abstimmung.set_legislaturperiode (int (row[rowids["periode"]]));
				abstimmung.set_abstimmungs_ergebnisse (abst_dict[abst_key])
				abstimmung.set_title ("Abstimmung:")
				abstimmung.add_tag ("Todo")
				abstimmung.add_category ("Todo")
				abstimmung.add_link ({"title": "bundestagslink", "url": "todo"})
				abstimmung.add_data_file ({"title": "Abstimmungsergebnis " + pdf_file, "url": "/res/abstimmungsliste/" + pdf_file})
				abstimmung.add_data_file ({"title": "Abstimmungsergebnis " + f, "url": "/res/abstimmungsliste/" + f})
				abstimmung.add_data_file ({"title": "Abstimmungsergebnis " + f[:-3] + "csv", "url": "/res/abstimmungsliste/csv/" + f[:-3] + "csv"})
				abstimmung.add_document ({"title": "Drucksache ", "url": "", "local": "/res/abstimmungsdaten/" + abst_key + "/"})
				
				pdf_file = os.path.join (xls_path, pdf_file)
				if os.path.isfile (pdf_file) and "pdf" in pdf_file:
					abstimmung.set_preview (get_pdf_preview (pdf_file))
				else:
					print "!!!! didn't fine pdf file for %s !!!!" % xls_file
				abstimmung.write_abstimmung (jekyll_file)


# write new summary table, see 3.2 oben
print "> updating summary table"
with open (summary_table, 'w') as f:
	f.write ("ABSTIMMUNG\t")
	for fraktion in fraktionen:
		f.write (fraktion + "\t")
	f.write ("file")
	f.write ("\n")
	
	for abstid in sorted (abst_dict):
		f.write (abstid + "\t")
		for fraktion in fraktionen:
			if fraktion in abst_dict[abstid] and abst_dict[abstid][fraktion]["ja"] + abst_dict[abstid][fraktion]["nein"] > 0:
				f.write (str (float (abst_dict[abstid][fraktion]["ja"]) / (abst_dict[abstid][fraktion]["ja"] + abst_dict[abstid][fraktion]["nein"])) + "\t")
			else:
				f.write ("0\t")
		f.write (abst_dict[abstid]["file"])
		f.write ("\n")

# write new json file, see 3.3 oben
print "> updating summary json"
with open (summary_json, 'w') as f:
	f.write (json.dumps (abst_dict, sort_keys=True, indent=2, separators=(',', ': ')))


