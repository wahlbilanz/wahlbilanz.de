# Abstimmungen

In diesem Verzeichnungen wurden Informationen zu den vergangenen Abstimmungen aus dem Bundestag zusammengetragen.
Die einzelnen Abstimmungen sind in Ordnern organisiert.
Die Ordner wurden nach dem Schema *Legislaturperiode-Sitzungsnummer-Absimmungsnummer* benannt.

Jeder Ordner enthaelt eine Datei im [YAML-Format](https://en.wikipedia.org/wiki/YAML).
Das Format ist machineslesbar, es gibt [Parser in vielen verschiedenen Sprachen](http://yaml.org/).

Mit Hilfe des Layouts in [../_layouts/abstimmung.html](../_layouts/abstimmung.html) uebersetzen wir die Dateien beispielsweise zu HTML-Seiten fuer das WahlBilanz.de Projekt,
Siehe zum Beispiel: [https://wahlbilanz.de/abstimmungen/018-003-01/](https://wahlbilanz.de/abstimmungen/018-003-01/) also Ueberseztung von [018-003-01/index.md](018-003-01/index.md).

In [abstimmungsparser.py](abstimmungsparser.py) stellen wir auch eine kleines Python-Script zur Verfügung, dass jeder gern benutzen kann um die Abstimmungsdaten selbst zu parsen und ggf. für andere Projekte zu nutzen. Um Beispielsweise die Titel aller Abstimmungen auszugeben würde folgendes Script genügen:

```python
abstimmungs_dir = '/pfad/zu/diesem/verzeichnis'

import os
import sys
sys.path.append (abstimmungs_dir)
from abstimmungsparser import Abstimmung


for subdir, dirs, files in os.walk (abstimmungs_dir):
  for directory in dirs:
    # abtimmungsverzeichnisse starten alle mit "018-"
    if "018-" in directory:
      # die abstimmungsdaten sind im file "index.md"
      abstimmuns_file = os.path.join (subdir, directory, "index.md")
      if os.path.isfile (abstimmuns_file):
        # abstimmung parsen und den titel ausgeben
        abstimmung = Abstimmung ()
        abstimmung.parse_abstimmung (abstimmuns_file)
        print abstimmung.get_title ()
```



Im Verzeichnis [applications](applications) gibt es auch ein paar Tools, die wir selbst geschrieben haben.
Die helfen dir vielleicht deine eigene Software zu schreiben :)

