from github import Github
import sys
import os
from os import listdir
abstimmungs_dir = '..'
sys.path.append (abstimmungs_dir)
from abstimmungsparser import Abstimmung

env_var="GITHUB_TOKEN"

if env_var not in os.environ:
  print ("need a GITHUB_TOKEN env")
  sys.exit(1)





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


g = Github(os.environ[env_var])

repo = g.get_repo("wahlbilanz/deinwal2021")
issues = repo.get_issues(state='all')
print(issues.totalCount)
existing = []
for issue in issues:
  #print(issue.title)
  existing.append (issue.title)

#print (existing)



for f in listdir (abstimmungs_dir):
  d = os.path.join (abstimmungs_dir, f)
  if os.path.isdir (d) and f.startswith('019'):
    abstimmungs_file = os.path.join (d, "index.md")
    if os.path.isfile (abstimmungs_file):
      #print (abstimmungs_file)
      abstimmung = Abstimmung ()
      abstimmung.parse_abstimmung (abstimmungs_file)
      abst_key = "%03d-%02d" % (abstimmung.get_bundestagssitzung(), abstimmung.get_abstimmung())

      title = abstimmung.get_title().replace ("Abstimmung: ", "") + " (019-" + abst_key + ")"

      if title in existing:
        continue


      #print (abstimmung.get_title().replace ("Abstimmung: ", ""))

      print ("creating ticket for " + title)



      text = "* Sitzung: "+str(abstimmung.get_bundestagssitzung())+"\n\
* Abstimmung: "+str(abstimmung.get_abstimmung())+"\n\
* Datum: "+str(abstimmung.get_datum()) + "\n\n\
### Ergebnis:\n\
\n\
Party | Ja | Nein | Enthaltungen | Ungültig | Nicht Abgegeben | Gesamt\n\
----- | -- | ---- | ------------ | -------- | --------------- | ------\n\
"
      ergebnisse = abstimmung.get_abstimmungs_ergebnisse ()
      #print (ergebnisse)
      for party in parties:
        text += party
        for decision in ["ja", "nein", "enthaltung","ungueltig","nichtabgegeben","gesamt"]:
          text += " | " + str(ergebnisse[party][decision])
        text += "\n"

      text += "\n### Documents:\n"
      docs = abstimmung.get_documents ()
      #print (docs)
      for d in docs:
        text += "* ["+d["title"]+"](https://wahlbilanz.de/"+d["local"]+")\n"

      text += "\n### Links:\n"
      text += "* Wahlbilanz: [019-"+abst_key+"](https://wahlbilanz.de/abstimmungen/019-"+abst_key+")\n"
      links = abstimmung.get_links ()
      #print (links)
      for l in links:
        text += "* ["+l["title"]+"]("+l["url"]+")\n"

      text += "### Preview:\n```\n" + abstimmung.get_preview() + "\n```"


      repo.create_issue(title=title, body=text)
      #print (text)
      #sys.exit(1)






