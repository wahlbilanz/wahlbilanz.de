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
import yaml

sys.path.append("../../../abstimmungen")
from abstimmungsparser import Abstimmung
import subprocess
import re
import requests
from bs4 import BeautifulSoup
import wikipedia

from categories import categories
from thesen import claims, claim_bundestagsids



wikipedia.set_lang("de")

DRUCKSACHEN = "https://dip21.bundestag.de/dip21/btd/19/"

abst_dict = {}
rowids = {}
fraktionen = []

bundestagspages_json = "../bundestag.de.json"

wd = os.path.dirname(os.path.realpath(__file__))
xls_path = os.path.join(wd, "../abstimmungsergebnisse")
csv_path = os.path.join(wd, "../abstimmungsergebnisse", "csv")
bundestagslinks = os.path.join(wd, "../bundestag.de")
drucksachen_path = os.path.join(wd, "../drucksachen")
if not os.path.isdir(csv_path):
  os.mkdir(csv_path)

xls_to_pdf = re.compile(r"^([0-9]+(_[0-9]+)?)_.*")
drucksachen_pattern = re.compile(r"\s19/([0-9]+)", re.MULTILINE)
drucksachen_url_pattern = re.compile(r"dip21.bundestag.de/dip21/btd/19/[0-9]+/([0-9]+).pdf", re.MULTILINE)

bundestagspages = {}

bundestags_extra_map = {
  "019-023-05": "509",
  "019-132-02": "643",
  "019-132-03": "644",
  "019-124-03": "628",
  "019-124-04": "629",
  "019-127-02": "633",
  "019-140-02": "657",
  "019-140-03": "658",
  "019-005-01": "493",
  "019-068-04": "563",
  "019-068-05": "564",
  "019-083-01": "574",
  "019-083-04": "581",
  "019-086-01": "583",
  "019-101-07": "603",
  "019-184-02": "691",
  "019-191-04": "699",
  "019-234-02": "746",
  "019-230-01": "741",
  "019-033-01": "514",
  "": "",
  "": "",
  "": "",
}


def getBundestagsTitle(soup):
  for i in soup.select(".bt-standard-content .bt-artikel__title"):
    return (''.join(i.findAll(text=True, recursive=False))).strip()


def getBundestagsDate(soup):
  for i in soup.select("article.bt-artikel .bt-artikel__title .bt-dachzeile"):
    return (''.join(i.findAll(text=True, recursive=False))).strip()


def getBundestagsText(soup):
  for i in soup.select("article.bt-artikel > p"):
    return i.text
    # (''.join(i.findAll(text=True, recursive=True))).strip()


def getBundestagsTextHTML(soup):
  for i in soup.select("article.bt-artikel > p"):
    return i.encode_contents().decode('UTF-8')
    # (''.join(i.findAll(text=True, recursive=True))).strip()


if os.path.isfile(bundestagspages_json):
  with open(bundestagspages_json) as data:
    bundestagspages = json.load(data)
    print('read ' + bundestagspages_json)

for f in listdir(bundestagslinks):
  if f not in bundestagspages:
    # print (f + " not in bundestagspages")
    if 'download' in f:
      continue
    with open(os.path.join(bundestagslinks, f)) as l:
      soup = BeautifulSoup(l, 'html.parser')
      o = {
        "id": f,
        "date": getBundestagsDate(soup),
        "title": getBundestagsTitle(soup),
        "text": getBundestagsText(soup),
        "textHTML": getBundestagsTextHTML(soup)
      }
      if o["title"] is not None:
        bundestagspages[f] = o
        save_bundestag = True
      else:
        print('error with meta of ' + f)
      # print (bundestagspages[f])
      # sys.exit(1)


def pandas_make_int(data, column):
  if column in data.columns:
    data = data.dropna(subset=[column])
    data.loc[column] = data[column].astype(int)


# convert excel crap to to csv, siehe step 2 oben
# def excel2csv(xls_file, csv_file):
#   print("  > converting %s to %s" % (xls_file, csv_file))
#   data = pandas.read_excel(xls_file, index_col=None)
#
#   if len(data) > 1000:
#     data = data.head(1000)
#
#   cols = ["Wahlperiode", "Sitzungnr", "Abstimmnr", "ja", "nein", "Enthaltung", "ungültig", "nichtabgegeben"]
#   for c in cols:
#     if c in data.columns:
#       data = data.dropna(subset=[c])
#       data[c] = data[c].astype(int)
#
#   data.to_csv(csv_file, encoding='utf-8', index=False)
#   return csv_file


# approach from 2017:
# as they define columnnames and sequence
# arbitarily and everytime differently
# we need to do this effort and match words...
def get_row_ids(header):
  rowids = {
    "periode": 0,
    "siztung": 1,
    "abstimmung": 2,
    "fraktion": 3,
    "ja": 7,
    "nein": 8,
    "enthaltung": 9,
    "ungueltig": 10,
    "nichtabgegeben": 11,
    "name": 4,
    "vorname": 5,
    "bezeichnung": 21,
  }

  for i in range(len(header)):
    columnname = header[i].lower()
    # print (str (i) + " -> " + columnname)
    if any(option in columnname for option in ["wahlperiode", "periode"]):
      rowids["periode"] = i
      continue
    if any(option in columnname for option in ["sitzungnr", "sitzungnummer", "sitzung"]):
      rowids["siztung"] = i
      continue
    if any(option in columnname for option in ["abstimmnr", "abstimmnummer", "abstimmung"]):
      rowids["abstimmung"] = i
      continue
    if any(option in columnname for option in ["fraktion", "gruppe"]):
      rowids["fraktion"] = i
      continue
    if any(option in columnname for option in ["ja"]):
      rowids["ja"] = i
      continue
    if any(option in columnname for option in ["nein"]):
      rowids["nein"] = i
      continue
    if any(option in columnname for option in ["enthaltung", "enthalten", "enthiel"]):
      rowids["enthaltung"] = i
      continue
    if any(option in columnname for option in ["ungueltig", "ungültig"]) or (
      "ung" in columnname and "ltig" in columnname):
      rowids["ungueltig"] = i
      continue
    if any(option in columnname for option in ["nichtabgegeben", "nichtabgg"]):
      rowids["nichtabgegeben"] = i
      continue
    if any(option == columnname for option in ["name", "nachname"]):
      rowids["name"] = i
      continue
    if any(option in columnname for option in ["vorname"]):
      rowids["vorname"] = i
      continue
    if any(option in columnname for option in ["bezeichnung"]):
      rowids["bezeichnung"] = i
      continue

  # print (rowids)
  return rowids


# see step 4 above
def get_pdf_preview(f):
  t = subprocess.check_output(["pdftotext", "-l", "1", f, "-"]).decode('UTF-8')
  i = t.find("Abgegebene Stimmen")
  if i > 0:
    t = t[:i]
  return t.strip()


def nDrucksachen(s):
  # print (s)
  # print (type(s))
  return drucksachen_url_pattern.findall(s)


def get_date_of_abstimmung(id_on_bundestag):
  # print (id_on_bundestag)
  return bundestagspages[id_on_bundestag]['date']


def find_bundestags_id(drucksachen, abst_key):
  if abst_key in bundestags_extra_map:
    return bundestags_extra_map[abst_key]
  print('searching for ' + str(drucksachen))
  i = None
  for btid in bundestagspages:
    t = bundestagspages[btid]['textHTML']
    if t is None:
      continue
    btp_drs = nDrucksachen(t)
    if len(btp_drs) != len(drucksachen):
      continue

    found = True
    for d in drucksachen:
      if d not in t:
        found = False
        break
    if not found:
      continue

    if i is not None:
      print("ERROR: found multiple bundestagsids")
      print(t)
      print(i)
      print(btid)
      sys.exit(1)
    i = btid
  return i


def get_date_of_abstimmung(id_on_bundestag):
  # print (id_on_bundestag)
  return bundestagspages[id_on_bundestag]['date']


def get_title_of_abstimmung(id_on_bundestag):
  # print (id_on_bundestag)
  return bundestagspages[id_on_bundestag]['title']
  # with open (os.path.join (bundestagslinks, id_on_bundestag)) as f:
  # soup = BeautifulSoup(f, 'html.parser')
  # for i in soup.select(".bt-standard-content .bt-artikel__title"):
  # return (''.join(i.findAll(text=True, recursive=False))).strip()
  # return "unknown"


def most_frequent(l):
  counter = 0
  num = l[0]
  for i in l:
    curr_frequency = l.count(i)
    if (curr_frequency > counter):
      counter = curr_frequency
      num = i
  return num


def fraktionsmapper(s):
  if "afd" in s:
    return {
      "name": "Alternative für Deutschland",
      "kuerzel": "AfD",
      "id": "afd",
      "color": "#009fe1",
      "picture": "afd.svg",
      "links": {
        "wikipedia": "https://de.wikipedia.org/wiki/AfD-Fraktion_im_Deutschen_Bundestag"
      },
      "shortDescription": "",
      "description": "",
            "positions": {},
        "order": 3,
    }
  if "bü90/gr" in s:
    return {
      "name": "Bündnis 90/Die Grünen",
      "kuerzel": "Grüne",
      "id": "buendnis-90-die-gruenen",
      "color": "#19a329",
      "picture": "gruene.svg",
      "links": {
        "wikipedia": "https://de.wikipedia.org/wiki/Bundestagsfraktion_B%C3%BCndnis_90/Die_Gr%C3%BCnen"
      },
      "shortDescription": "",
      "description": "",
            "positions": {},
        "order": 6,
    }
  if "cdu/csu" in s:
    return {
      "name": "Unionsparteien CDU/CSU",
      "kuerzel": "CDU/CSU",
      "id": "cdu-csu",
      "color": "#000000",
      "picture": "cdu-csu.svg",
      "links": {
        "wikipedia": "https://de.wikipedia.org/wiki/CDU/CSU-Fraktion_im_Deutschen_Bundestag"
      },
      "shortDescription": "",
      "description": "",
            "positions": {},
        "order": 1,
    }
  if "die linke." in s:
    return {
      "name": "Die Linke",
      "kuerzel": "DIE LINKE",
      "id": "die-linke",
      "color": "#e0001a",
      "picture": "linke.svg",
      "links": {
        "wikipedia": "https://de.wikipedia.org/wiki/Fraktion_Die_Linke_im_Bundestag#Zusammensetzung_im_19._Deutschen_Bundestag"
      },
      "shortDescription": "",
      "description": "",
            "positions": {},
        "order": 5,
    }
  if "fdp" in s:
    return {
      "kuerzel": "FDP",
      "name": "Freie Demokratische Partei",
      "id": "fdp",
      "color": "#ffee00",
      "picture": "fdp.svg",
      "links": {
        "wikipedia": "https://de.wikipedia.org/wiki/Fraktion_der_Freien_Demokraten"
      },
      "shortDescription": "",
      "description": "",
            "positions": {},
        "order": 4,
    }
  if "fraktionslos" in s:
    return {
      "name": "Fraktionslos",
      "kuerzel": "fraktionslos",
      "id": "fraktionslos",
      "color": "#999999",
      "picture": "",
      "links": {
        "wikipedia": "https://de.wikipedia.org/wiki/Fraktionsloser_Abgeordneter"
      },
      "shortDescription": "",
      "description": "",
            "positions": {},
        "order": 10,
    }
  if "spd" in s:
    return {
      "name": "Sozialdemokratische Partei Deutschlands",
      "kuerzel": "SPD",
      "id": "spd",
      "color": "#ff481f",
      "picture": "spd.svg",
      "links": {
        "wikipedia": "https://de.wikipedia.org/wiki/SPD-Bundestagsfraktion"
      },
      "shortDescription": "",
      "description": "",
            "positions": {},
        "order": 2,
    }
  return s


def replace_non_alphanum(s):
  return re.sub('[^0-9a-zA-Z]+', '-', s)


print('start')
candidates = {}
# claims = []
# n2 = 0


def candidate_id(row, rowids):
  return replace_non_alphanum(
    row[rowids["name"]] + "_" + row[rowids["vorname"]] + "_" + fraktionsmapper(row[rowids["fraktion"]].lower())["id"])


def optionally_invert_result (result, invert):
  if invert:
    return -result
  return result


# siehe step 1 oben
for f in listdir(csv_path):
  # print ("> checking %s" % f)
  if not "xls-data.csv" in f and not "xls-datacsv" in f:
    continue

  # xls_file = os.path.join(xls_path, f)
  csv_file = os.path.join(csv_path, f)

  print("> processing %s" % f)

  # n = 0

  # parse csv, siehe 3. oben
  print("  > parsing values CSV")
  with open(csv_file, 'r') as csvfile:
    dialect = csv.Sniffer().sniff(csvfile.read(1024), delimiters=";,")
    csvfile.seek(0)
    table = csv.reader(csvfile, dialect)
    # table = csv.reader (csvfile)
    abst_key = None

    # go through the table
    for row in table:
      # parse row sequence...
      if "Wahlperiode" in row or "Vorname" in row or "Bemerkung" in row:
        rowids = get_row_ids(row)
        continue

      # print (row[rowids["periode"]], row[rowids["siztung"]], row[rowids["abstimmung"]])
      if abst_key is None:
        abst_key = "%03d-%03d-%02d" % (
          int(row[rowids["periode"]]), int(row[rowids["siztung"]]), int(row[rowids["abstimmung"]]))
      if abst_key != "%03d-%03d-%02d" % (
        int(row[rowids["periode"]]), int(row[rowids["siztung"]]), int(row[rowids["abstimmung"]])):
        print("different abst_key!?")
        print(abst_key)
        print(
          "%03d-%03d-%02d" % (int(row[rowids["periode"]]), int(row[rowids["siztung"]]), int(row[rowids["abstimmung"]])))
        sys.exit(1)

      if abst_key not in claim_bundestagsids:
        abst_key = None
        continue

      claim = None
      for c in claims:
        if c['bundestagsid'] == abst_key:
          claim = c

      assert (claim is not None)

      fraktion = fraktionsmapper(row[rowids["fraktion"]].lower())
      fraktionsid = fraktion["kuerzel"]

      if fraktionsid == 'fraktionslos':
        continue

      if fraktion not in fraktionen:
        fraktionen.append(fraktion)

      if abst_key not in abst_dict:
        abst_dict[abst_key] = {}
      abst_dict[abst_key]["file"] = f

      if fraktionsid not in abst_dict[abst_key]:
        abst_dict[abst_key][fraktionsid] = {"ja": 0, "nein": 0, "enthaltung": 0, "ungueltig": 0, "nichtabgegeben": 0,
                                            "gesamt": 0}

      abst_dict[abst_key][fraktionsid]["ja"] += int(row[rowids["ja"]])
      abst_dict[abst_key][fraktionsid]["nein"] += int(row[rowids["nein"]])
      abst_dict[abst_key][fraktionsid]["enthaltung"] += int(row[rowids["enthaltung"]])
      abst_dict[abst_key][fraktionsid]["ungueltig"] += int(row[rowids["ungueltig"]])
      abst_dict[abst_key][fraktionsid]["nichtabgegeben"] += int(row[rowids["nichtabgegeben"]])
      abst_dict[abst_key][fraktionsid]["gesamt"] += 1

      cid = candidate_id(row, rowids)
      if cid not in candidates:
        candidates[cid] = {
          "id": candidate_id(row, rowids),
          "publishPersonalInfo": True,
          "name": row[rowids["bezeichnung"]],
          "party": fraktionsid,
          "positions": {}
        }
      # print(candidate)
      # print(yaml.dump(candidate))
      # print(row)
      candidates[cid]["positions"][abst_key] = {
        "vote": optionally_invert_result(int(row[rowids["ja"]]) - int(row[rowids["nein"]]), claim["invert"])
      }




      # n = n + 1
      # if n > 3:
      #   break

    if abst_key is None:
      continue

    print("  > " + abst_key)
    sum_votes = 0
    for fraktion in fraktionen:
      sum_votes += abst_dict[abst_key][fraktion["kuerzel"]]["gesamt"]
    if sum_votes > 709:
      print("there seems to be an error! more than 709 votes for " + f[:-4] + " (" + abst_key + ")")
      sys.exit(1)

    pdf_file = xls_to_pdf.sub("\\1-data.pdf", f)
    print(" > extracting text from PDF " + pdf_file)
    pdf_preview = get_pdf_preview(os.path.join(xls_path, pdf_file)).replace("19714672", "19/14672")
    # abst_dict[abst_key]["pdf_file"] = pdf_file
    # abst_dict[abst_key]["pdf_text"] = pdf_preview

    # welche drucksachen gehoeren dazu?
    drucksachen = []
    # print(pdf_preview)
    drs = drucksachen_pattern.findall(pdf_preview)

    if "20180322_5" in pdf_file:
      drs = ["1096", "1304"]
    elif "20181108_4" in pdf_file:
      drs = ["4723", "5583", "5607"]
    elif "20201118_4" in pdf_file:
      drs = ["24387"]

    if len(drs) < 1:
      if "20180517-data" in pdf_file or "20210520_1" in pdf_file:
        print("no drucksachen fuer den einspruch...")
      else:
        print("oops! no drucksachen!?: " + f)
        sys.exit(1)

    # print (drs)
    # print (drs)
    for d in drs:
      while len(d) < 5:
        d = "0" + d
      drs_url = DRUCKSACHEN + d[:3] + "/19" + d + ".pdf"
      drs_path = os.path.join(drucksachen_path, d + ".pdf")
      drucksachen.append({"id": d, "url": drs_url})

      # potential_bundestagsids += find_bundestags_ids (drs_url)
      # print (potential_bundestagsids)

      # # download drucksache
      # if isfile(drs_path):
      #   # we already downloaded this file
      #   # print "- ignoring %s as it is already converted..." % f
      #   continue
      # r = requests.get(drs_url)
      # with open(drs_path, 'wb') as output_file:
      #   output_file.write(r.content)

    potential_bundestagsid = find_bundestags_id(drs, abst_key)
    if potential_bundestagsid is None:
      print('no bundestagsid for')
      print(drs)
      sys.exit(1)

    # if len(potential_bundestagsids) < 1:
    # print ("oops! no bundestagsid: " + f)
    # sys.exit(1)
    # id_on_bundestag = most_frequent(potential_bundestagsids)
    # print ('ids')
    # print (potential_bundestagsids)
    # print (potential_bundestagsid)
    # print (id_on_bundestag)

    abstimmungstitle = get_title_of_abstimmung(potential_bundestagsid)
    abstimmungsdate = get_date_of_abstimmung(potential_bundestagsid)
    print(str(potential_bundestagsid) + " -> " + abstimmungstitle + ' -> ' + abstimmungsdate)

    # print (abst_dict)

    # break

    # # create new page, see 3.1 oben
    # jekyll_file = os.path.abspath(os.path.join(wd, "../../abstimmungen/" + abst_key + "/index.md"))
    # abstimmung = Abstimmung()
    # if not os.path.isfile(jekyll_file):
    #   print("  > erstelle neue abstimmungsseite " + jekyll_file)
    #   abstimmung.add_tag("Todo")
    #   abstimmung.add_category("Todo")
    # else:
    #   print("  > lese existierende abstimmungsseite " + jekyll_file)
    #   abstimmung.parse_abstimmung(jekyll_file)
    #
    # abstimmung.set_abstimmung(int(row[rowids["abstimmung"]]));
    # abstimmung.set_bundestagssitzung(int(row[rowids["siztung"]]));
    # abstimmung.set_legislaturperiode(int(row[rowids["periode"]]));
    # abstimmung.set_abstimmungs_ergebnisse(abst_dict[abst_key])
    # abstimmung.set_title("Abstimmung: " + abstimmungstitle)
    # abstimmung.add_link({"title": "Link zu bundestag.de",
    #                      "url": "https://www.bundestag.de/parlament/plenum/abstimmung/abstimmung?id=" + potential_bundestagsid})
    # abstimmung.set_datum(abstimmungsdate)
    #
    # datafiles = abstimmung.get_data_files()
    # # TODO: check if the files are not there yet!
    # abstimmung.add_data_file(
    #   {"title": "Abstimmungsergebnis " + pdf_file, "url": "/res/2021-btw/abstimmungsergebnisse/" + pdf_file})
    # abstimmung.add_data_file({"title": "Abstimmungsergebnis " + f, "url": "/res/2021-btw/abstimmungsergebnisse/" + f})
    # abstimmung.add_data_file({"title": "Abstimmungsergebnis " + f[:-4] + "csv",
    #                           "url": "/res/2021-btw/abstimmungsergebnisse/csv/" + f[:-4] + "csv"})
    # for d in drucksachen:
    #   abstimmung.add_document({"title": "Drucksache 19/" + d["id"], "url": d["url"],
    #                            "local": "/res/2021-btw/drucksachen/" + d["id"] + ".pdf"})
    #
    # abstimmung.set_preview(pdf_preview)
    # abstimmung.write_abstimmung(jekyll_file)
    claimslinks = [{
      "title": "Datum der Abstimmung: " + abstimmungsdate
    }, {
      "title": "Link zu bundestag.de",
      "url": "https://www.bundestag.de/parlament/plenum/abstimmung/abstimmung?id=" + potential_bundestagsid
    }
    ]
    for d in drucksachen:
      claimslinks.append({
        "title": "Drucksache 19/" + d["id"],
        "url": d["url"]
      })

    # claims.append({
    #   "id": abst_key,
    #   "order": n2 + 1,
    #   "title": abstimmungstitle,
    #   "description": "...",
    #   "category": "all",
    #   "links": claimslinks
    # })
    # n2 = n2 + 1

    # if n2 > 60:
    #   break

  # break

# double check that we do not have double entries
# for abstid in sorted(abst_dict):
#   sum_votes = 0
#   for fraktion in fraktionen:
#     if fraktion in abst_dict[abstid]:
#       sum_votes += abst_dict[abstid][fraktion]["gesamt"]
#   if sum_votes > 709:
#     print("there seems to be an error! more the 709 votes for " + abstid)
#     sys.exit(1)
#
# print(json.dumps(abst_dict, sort_keys=True, indent=2, separators=(',', ': ')))

# print("N2:", n2)

bundeswehr_n = 0
bundeswehr_id = "bundeswehr"
bundeswehrclaim = {
    "bundestagsid": bundeswehr_id,
    "category": "internationales",
    "description": "Die Bundeswehr wurde in der letzen Legislaturperiode in den folgenden Ländern eingesetzt: Irak, Jordanien, Syrien, Mittelmeer, Libanon, Mali, Afghanistan, Somalia, Südsudan, Kosovo, Dafur.",
    "id": bundeswehr_id,
    "order": 6,
    "shorttitle":"Bundeswehreinsätze",
    "title": "Bundeswehreinsätze in diesen Gebieten sind gerechtfertigt."
}

for claim in claims:
  if claim["category"] == "bundeswehr":
    # print (claim["bundestagsid"])
    bundeswehr_n = bundeswehr_n + 1
    for candidate in candidates:
      if bundeswehr_id not in candidates[candidate]["positions"]:
        candidates[candidate]["positions"][bundeswehr_id] = {
          "vote": 0,
          "n": 0
        }
      # print (candidates[candidate]["positions"][bundeswehr_id])
      if claim["bundestagsid"] in candidates[candidate]["positions"]:
        candidates[candidate]["positions"][bundeswehr_id]["n"] = candidates[candidate]["positions"][bundeswehr_id]["n"] + 1
        candidates[candidate]["positions"][bundeswehr_id]["vote"] = candidates[candidate]["positions"][bundeswehr_id]["vote"] + candidates[candidate]["positions"][claim["bundestagsid"]]["vote"]
        del candidates[candidate]["positions"][claim["bundestagsid"]]


claims.append(bundeswehrclaim)


for candidate in candidates:
  # print (candidate, candidates[candidate]["positions"][bundeswehr_id]["n"], candidates[candidate]["positions"][bundeswehr_id]["vote"])
  assert(candidates[candidate]["positions"][bundeswehr_id]["n"] >= candidates[candidate]["positions"][bundeswehr_id]["vote"])
  if candidates[candidate]["positions"][bundeswehr_id]["n"] > 0:
    candidates[candidate]["positions"][bundeswehr_id]["vote"] = round(candidates[candidate]["positions"][bundeswehr_id]["vote"] / candidates[candidate]["positions"][bundeswehr_id]["n"])
    del candidates[candidate]["positions"][bundeswehr_id]["n"]
    assert(candidates[candidate]["positions"][bundeswehr_id]["vote"] <= 1)




cs = []
for c in candidates:
  cs.append(candidates[c])


for p in fraktionen:
    n_candidates = 0
    # print (p)
    # print (fraktionen)
    for candidate in candidates:
        # print(candidate, candidates[candidate]["party"], p["kuerzel"], len(candidates[candidate]["positions"]))
        if candidates[candidate]["party"] == p["kuerzel"] and len(candidates[candidate]["positions"]) > 0:
            n_candidates += 1
    # print ("n_candidates", n_candidates)
    if n_candidates > 0:
        for claim in claims:
            if claim["category"] == "bundeswehr":
              continue
            s = 0
            for candidate in candidates:
                # print (candidates[candidate]["party"], p["id"], len(candidates[candidate]["positions"]), claim['bundestagsid'], candidates[candidate]["positions"], claim['id'] in candidates[candidate]["positions"])
                if candidates[candidate]["party"] == p["kuerzel"] and len(candidates[candidate]["positions"]) > 0 and claim['bundestagsid'] in candidates[candidate]["positions"]:
                    # print('x', candidates[candidate]["positions"][claim['bundestagsid']])
                    s += candidates[candidate]["positions"][claim['bundestagsid']]["vote"]
            # print('p', claim)
            # print('p', parties[p])
            p["positions"][claim['bundestagsid']] = {
                "vote": s / n_candidates
            }
            # print (p["positions"][claim['bundestagsid']])



with open('candidates.yaml', 'w') as f:
  print(yaml.dump({"candidates": cs}, f, sort_keys=False, default_flow_style=False))

with open('claims.yaml', 'w') as f:
  print(yaml.dump({"claims": claims}, f, sort_keys=False, default_flow_style=False))

with open('parties.yaml', 'w') as f:
  print(yaml.dump({"parties": fraktionen}, f, sort_keys=False, default_flow_style=False))

with open('categories.yaml', 'w') as f:
  print(yaml.dump({"categories": categories
  }, f, sort_keys=False, default_flow_style=False))




political_candidates = {}
personal_candidates = {}


def get_value_of_candidate(candidate, key):
    if key in candidate:
        return candidate[key]
    return None


for c in candidates:
    political_candidates[c] = {
      "party": get_value_of_candidate(candidates[c], "party"),
      "listOrder": get_value_of_candidate(candidates[c], "listOrder"),
      "positions": get_value_of_candidate(candidates[c], "positions")
    }
    personal_candidates[c] = {
        "name": get_value_of_candidate(candidates[c], "name"),
        "picture": get_value_of_candidate(candidates[c], "picture"),
        # "shortDescription": get_value_of_candidate(candidates[c], "shortDescription"),
        # "description": get_value_of_candidate(candidates[c], "description"),
        # "links": get_value_of_candidate(candidates[c], "links"),
        "color1": get_value_of_candidate(candidates[c], "color1"),
        "color2": get_value_of_candidate(candidates[c], "color2"),
    }


claim_map = {}
for c in claims:
  c["id"] = c["bundestagsid"]
  if c["category"] != "bundeswehr":
    claim_map[c["id"]] = c

category_map = {}
for c in categories:
  category_map[c["id"]] = c

party_map = {}
for f in fraktionen:
  if f["kuerzel"] == 'fraktionslos':
    continue
  f["id"] = f["kuerzel"]
  party_map[f["id"]] = f

politicalData = {
    "parties": party_map,
    "claims": claim_map,
    "categories": category_map,
    "candidates": political_candidates
}


with open('personal.json', 'w') as json_file:
    json.dump(personal_candidates, json_file, indent=2, sort_keys=True)
    # json.dump(personal_candidates, json_file)

with open('political.json', 'w') as json_file:
    json.dump(politicalData, json_file, indent=2, sort_keys=True)
    # json.dump(politicalData, json_file)




