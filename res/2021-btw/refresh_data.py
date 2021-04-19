#!/usr/bin/env python3
#
# dieses script hilft die verteilten daten zu den abstimmungen in der wahlbilanzseite zusammen zu fuehren.
# es tut prinzipiell:
#
# 1. suche nach XLS files die noch nicht konvertiert wurden
# 2. konvertiere nach CSV
# 3. parse CSV
# 4. parse PDF und extrahiere drucksachen
# 5. downloade drucksachen
# 6. finde link zur uebersicht auf bundestag.de
# 7. schreib wissen auf
#   7.1 erstelle dummy page in /abstimmungen
#   7.2 update summary.table
#   7.3 update summary.json


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
import requests
from bs4 import BeautifulSoup

DRUCKSACHEN="https://dip21.bundestag.de/dip21/btd/19/"

abst_dict = {}
rowids = {}
fraktionen = []

summary_json = "summary.json"
summary_table = "summary.table"

wd = os.path.dirname (os.path.realpath(__file__))
xls_path = os.path.join (wd, "abstimmungsergebnisse")
csv_path = os.path.join (wd, "abstimmungsergebnisse", "csv")
bundestagslinks = os.path.join (wd, "bundestag.de")
drucksachen_path = os.path.join (wd, "drucksachen")
if not os.path.isdir(csv_path):
  os.mkdir(csv_path)

xls_to_pdf = re.compile(r"^([0-9]+_[0-9]+)_.*")
drucksachen_pattern = re.compile(r" 19/([0-9]+)", re.MULTILINE)


# convert excel crap to to csv, siehe step 2 oben
def excel2csv (xls_file, csv_file):
  print ("  > converting %s to %s" % (xls_file, csv_file))
  data = pandas.read_excel (xls_file, index_col=None)
  data.to_csv (csv_file, encoding='utf-8', index=False)
  return csv_file


# approach from 2017:
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

# see step 4 above
def get_pdf_preview (f):
  return str (subprocess.check_output (["pdftotext", "-l", "1", f, "-"]))

# find the link id of an abstimmung given a drucksache... m(
def find_bundestags_id (drucksache):
  for f in listdir (bundestagslinks):
    with open (os.path.join (bundestagslinks, f)) as l:
      if drucksache in l.read ():
        return f
  return "-1"

def get_title_of_abstimmung(id_on_bundestag):
  with open (os.path.join (bundestagslinks, id_on_bundestag)) as f:
    soup = BeautifulSoup(f, 'html.parser')
    for i in soup.select(".bt-standard-content .bt-artikel__title"):
      return (''.join(i.findAll(text=True, recursive=False))).strip()
  return "unknown"


# were there results before?
if os.path.isfile (summary_json):
  with open (summary_json) as data:
    abst_dict = json.load(data)
    for abst in abst_dict:
      for fraktion in abst_dict[abst]:
        if fraktion not in fraktionen and fraktion != "file":
          fraktionen.append (fraktion)



# siehe step 1 oben
for f in listdir (xls_path):
  if not "xls-data.xlsx" in f or "lock" in f:
    continue

  xls_file = os.path.join (xls_path, f)
  csv_file = os.path.join (csv_path, f[:-4] + "csv")

  if isfile (csv_file):
    # we already processed this file
    #print "- ignoring %s as it is already converted..." % f
    continue

  print ("> processing %s" % f)

  # convert to csv, siehe 2. oben
  print ("  > converting to CSV")
  excel2csv (xls_file, csv_file)


  # parse csv, siehe 3. oben
  print ("  > parsing values CSV")
  with open(csv_file, 'r') as csvfile:
      dialect = csv.Sniffer ().sniff (csvfile.read(1024), delimiters = ";,")
      csvfile.seek (0)
      table = csv.reader (csvfile, dialect)
      #table = csv.reader (csvfile)

      # go through the table
      for row in table:
        # parse row sequence...
        if "Wahlperiode" in row or "Vorname" in row or "Bemerkung" in row:
          rowids = get_row_ids (row)
          continue


        abst_key = "%03d-%03d-%02d" % (int (row[rowids["periode"]]), int (row[rowids["siztung"]]), int (row[rowids["abstimmung"]]))
        fraktion = row[rowids["fraktion"]]

        #if 'B' in fraktion and 'gr' in fraktion.lower ():
          #fraktion = 'Gruenen'

        #if 'linke' in fraktion.lower ():
          #fraktion = 'die.linke'

        fraktion = fraktion.lower ()

        if fraktion not in fraktionen:
          fraktionen.append (fraktion)

        if abst_key not in abst_dict:
          abst_dict[abst_key] = {}
        #abst_dict[abst_key]["file"] = f

        if fraktion not in abst_dict[abst_key]:
          abst_dict[abst_key][fraktion] = { "ja": 0, "nein": 0, "enthaltung": 0, "ungueltig": 0, "nichtabgegeben": 0, "gesamt": 0 }

        abst_dict[abst_key][fraktion]["ja"] += int (row[rowids["ja"]])
        abst_dict[abst_key][fraktion]["nein"] += int (row[rowids["nein"]])
        abst_dict[abst_key][fraktion]["enthaltung"] += int (row[rowids["enthaltung"]])
        abst_dict[abst_key][fraktion]["ungueltig"] += int (row[rowids["ungueltig"]])
        abst_dict[abst_key][fraktion]["nichtabgegeben"] += int (row[rowids["nichtabgegeben"]])
        abst_dict[abst_key][fraktion]["gesamt"] += 1

      sum_votes = 0
      for fraktion in fraktionen:
        sum_votes += abst_dict[abst_key][fraktion]["gesamt"]
      if sum_votes > 709:
        print ("there seems to be an error! more than 709 votes for " + f[:-4] + " (" + abst_key + ")")
        sys.exit (1)

      print (" > extracting text from PDF")
      pdf_file = xls_to_pdf.sub ("\\1-data.pdf", f)
      pdf_preview = get_pdf_preview (os.path.join (xls_path, pdf_file))
      #abst_dict[abst_key]["pdf_file"] = pdf_file
      #abst_dict[abst_key]["pdf_text"] = pdf_preview

      id_on_bundestag = None

      # welche drucksachen gehoeren dazu?
      drucksachen = []
      print (pdf_preview)
      drs = drucksachen_pattern.findall(pdf_preview)
      if len(drs) < 1:
        print ("oops! no drucksachen!?: " + f)
        sys.exit(1)
      print (drs)
      for d in drs:
        while len(d) < 5:
          d = "0" + d
        drs_url = DRUCKSACHEN + d[:3] + "/19" + d + ".pdf"
        drs_path = os.path.join (drucksachen_path, d + ".pdf")
        # download drucksache
        if isfile (drs_path):
          # we already downloaded this file
          #print "- ignoring %s as it is already converted..." % f
          continue
        r = requests.get(drs_url)
        with open(drs_path,'wb') as output_file:
          output_file.write(r.content)
        drucksachen.append({"id": d, "url": drs_url})
        #print(d, drs_url, drs_path)

        potential_bundestagsid = find_bundestags_id (drs_url)

        if id_on_bundestag is None:
          id_on_bundestag = potential_bundestagsid
        if id_on_bundestag != potential_bundestagsid:
          print ("oops! missmatch on bundestagsid!?: " + id_on_bundestag + " vs " + potential_bundestagsid + " for " + f)
          sys.exit(1)

      if id_on_bundestag is None:
        print ("oops! no bundestagsid: " + f)
        sys.exit(1)

      abstimmungstitle = get_title_of_abstimmung(id_on_bundestag)


      print (abst_dict)

      #break

      # create new page, see 3.1 oben
      jekyll_file = os.path.abspath (os.path.join (wd, "../../abstimmungen/" + abst_key + "/index.md"))
      abstimmung = Abstimmung ()
      if not os.path.isfile (jekyll_file):
        print ("  > erstelle neue abstimmungsseite " + jekyll_file)
        abstimmung.add_tag ("Todo")
        abstimmung.add_category ("Todo")
      else:
        print ("  > lese existierende abstimmungsseite " + jekyll_file)
        abstimmung.parse_abstimmung (jekyll_file)

      abstimmung.set_abstimmung (int (row[rowids["abstimmung"]]));
      abstimmung.set_bundestagssitzung (int (row[rowids["siztung"]]));
      abstimmung.set_legislaturperiode (int (row[rowids["periode"]]));
      abstimmung.set_abstimmungs_ergebnisse (abst_dict[abst_key])
      abstimmung.set_title ("Abstimmung: " + abstimmungstitle)
      abstimmung.add_link ({"title": "Link zu bundestag.de", "url": "https://www.bundestag.de/parlament/plenum/abstimmung/abstimmung?id=" + id_on_bundestag})

      datafiles = abstimmung.get_data_files()
      # TODO: check if the files are not there yet!
      abstimmung.add_data_file ({"title": "Abstimmungsergebnis " + pdf_file, "url": "/res/2021-btw/abstimmungsergebnisse/" + pdf_file})
      abstimmung.add_data_file ({"title": "Abstimmungsergebnis " + f, "url": "/res/2021-btw/abstimmungsergebnisse/" + f})
      abstimmung.add_data_file ({"title": "Abstimmungsergebnis " + f[:-4] + "csv", "url": "/res/2021-btw/abstimmungsergebnisse/csv/" + f[:-4] + "csv"})
      for d in drucksachen:
        abstimmung.add_document ({"title": "Drucksache 19/" + d["id"], "url": d["url"], "local": "/res/2021-btw/drucksachen/" + d["id"] + ".pdf"})

      abstimmung.set_preview (pdf_preview.decode('ascii'))
      abstimmung.write_abstimmung (jekyll_file)

  break

