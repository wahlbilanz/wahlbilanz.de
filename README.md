# WahlBilanz.de

Dieses Repository ist der Quellcode zur Website von [WahlBilanz.de](https://wahlbilanz.de/).


## Hintergrung

Die Website ist als "Nebenprodukt" von einem anderen Projekt entstanden:
Für [DeinWal.de](https://deinwal.de) mussten wir jede Menge Daten und Dokumente von verschiedenen Webseiten zu Abstimmungen im Bundestag zusammenführen, kategorisieren und taggen.
Das war natürlich mit sehr viel manueller Arbeit verbunden.
Die meisten Daten sind im Zuge von Open Data und E-Government Initiativen zwar online und frei zugänglich aber häufig schlecht verlinkt und stehen manchmal in sehr komischen Formaten zur Verfügung.
Zum Beispiel gibt es auf [bundestag.de zwar eine hübsche Seite, die die Abstimmung zur Einführung eines Mindestlohns visualisiert](https://www.bundestag.de/parlament/plenum/abstimmung/abstimmung?id=290), die rohen Abstimmungsdaten sind dort aber nicht verlinkt.
Die [Rohdaten muss man sich von einer anderen Seite laden](https://www.bundestag.de/parlament/plenum/abstimmung/liste).
Für die Zuordnung von Daten zu Abstimmungen ist auch einiges an manuellem Aufwand nötig.
Und ist endlich der passende Datensatz gefunden, sind die Abstimmungsergebnisse in einer PDF-Datei gefangen ([originales Dokument](https://www.bundestag.de/blob/286286/8830dd61852c3588376a1f5ba6531dce/20140703_2-data.pdf)):

![Abstimmungsdaten als PDF...](/img/2017-06-undlos/montage-preview.png)


Alternativ stehen die [Daten auch im proprietären Excel-Format](https://www.bundestag.de/blob/286290/de77f65674a3bd51f02fd1b9a7dbc915/20140703_2_xls-data.xls) zur Verfügung.
Beides nichts womit Free-Software-Fans arbeiten möchten... ;-)

Wir haben die Daten also über Wochen mühsam gesammelt, integriert, konvertiert, getaggt ... usw.
Wir sind aber bestimmt nicht die einzigen, die vor dem Problem stehen!
Damit sich aber nicht jeder andere die gleiche Arbeit machen muss entschieden wir uns alles auf eine Website zu stellen.

So entstand die Idee zu [WahlBilanz.de](https://wahlbilanz.de/).

Hier findet ihr [alle Abstimmungen der aktuellen Legislaturperiode im Bundestag](https://wahlbilanz.de/abstimmungen/).
Zu jeder Abstimmung gibt es noch [eine Detail-Seite, die mehr Informationen und Links zu anderen Seiten sammelt und bereit stellt](https://wahlbilanz.de/abstimmungen/018-046-02/).


## Mach Mit!

Das coolste ist: [Du kannst mitmachen](https://wahlbilanz.de/contribute/)! :)

* Du kannst uns **Analysen zu bestimmten Themen/Abstimmung/Vorkommnissen** schicken, die wir dann als Artikel unter deinem Namen veröffentlichen. Wir nehmen auch gern Links zu Beiträgen, die du vielleicht schon in deinem Blog veröffentlicht hast?
* Du kannst probieren das **Layout der Seite** zu verbessern. Vielleicht hast du eine bessere Idee für ein Logo? Oder bist ein CSS-Profi?
* Du kannst uns helfen **mehr Informationen** zu den Abstimmungen (z.B. weiterführende Links etc.) oder anderen Daten zu sammeln.
* Du kannst **Fehler finden und verbessern!** Wir sind natürlich auch nur Menschen und bei weitem nicht perfekt... Wenn dir etwas auffällt - sei es Rechtschreibfehler, falsche Kategorisierung, Layoutprobleme etc - fänden wir es super, wenn du uns informierst und/oder beim Beheben hilfst! :)
* Du kannst natürlich auch dabei helfen **WahlBilanz.de bekannt zu machen!** Erzähl einfach allen davon.. Freunden, Familie, Kollegen, Politikern, Journalisten, Schauspielern, Ärzten, Barkeepern, Gärtnern, ..... :)

Dir fallen bestimmt noch viele andere Möglichkeiten ein..
Du solltest jedoch immer darauf achten, dass du unparteiisch bleibst!
Diese Seite soll informieren und nicht beeinflussen.
Wenn du etwas analysieren möchtest solltest du deine Vorgehensweise, die Herkunft der Daten, und deine Entscheidungen gut dokumentieren.

Deine Beiträge kannst du zum Beispiel mit einer E-Mail einsenden, unsere [Kontaktdaten findest du auf der Webseite](https://wahlbilanz.de/about/).
Oder du [forkst das Repository](https://github.com/wahlbilanz/wahlbilanz.de) und reichst deine Vorschläge, Verbesserungen, und Artikel direkt als Pull-Request ein.

Wer Lust hat die Seite aktiv mitzugestalten kann auch gern dem [WahlBilanz.de-Team](https://github.com/orgs/wahlbilanz/teams/wahlbilanz-team) beitreten :)


## Projekt kompilieren

WahlBilanz.de basiert auf [Jekyll](http://jekyllrb.com/) und generiert eine statische Seite.
Das ist das gleiche System, dass auch [GitHub Pages](http://jekyllrb.com/docs/github-pages/) verwendet.
In dem Repository hier sieht man nur den Source-Code der Webseite; er ist zum größten Teil in [Markdown](https://en.wikipedia.org/wiki/Markdown) verfasst.
Um daraus HTML-Seiten zu generieren musst du das Projekt noch "kompilieren".
Also zunächst das Projekt von GitHub clonen:

    git clone https://github.com/wahlbilanz/wahlbilanz.de

Dann noch fix die Git-Submodule initialisieren:

    git submodule update --recursive --init

Und dann ist alles bereit zum kompilieren!
Dafür gibt es mehrere Möglichkeiten - alle generieren am Ende ein `_site` Verzeichnis, das von einem Webserver ausgeliefert werden kann.

### Typisches Setup mit Jekyll

Eine Anleitung für eine Installation von Jekyll gibt es zum Beispiel auf [jekyllrb.com/docs/installation](https://jekyllrb.com/docs/installation/).
Im Prinzip reicht der folgende Befehl:

    gem install jekyll

(Für [Windows-Nutzer ist es aber ein bisschen komplizierter](https://jekyllrb.com/docs/windows/).)

Wenn Jekyll installiert ist, kann man die Seite ganz einfach mit dem folgenden Befehl übersetzen:

    jekyll build

Weitere [Tricks und Features findet ihr auf jekyllrb.com/docs/usage](https://jekyllrb.com/docs/usage/).

### Benutzung mit Docker

Wenn ihr [Docker](https://www.docker.com/) installiert habt ist das alles viel einfacher.
Angenommen das WahlBilanz.de-Projekt befindet sich in `/pfad/zu/wahlbilanz.de`, dann genügt der folgende Aufruf:

    docker run --rm -v /pfad/zu/wahlbilanz.de:/jekyll binfalse/jekyll

Docker kümmert sich um den Rest! :)

In jedem Fall solltest du jetzt ein `_site` Verzeichnis sehen in dem die Webseiten im HTML-Format liegen.
Sollte das irgendwie nicht geklappt haben kannst du dich gern bei uns melden!
Dann versuchen wir dir zu helfen und überarbeiten diese Anleitung :)


## Lizenz

Die Webseite wird unter der [Creative Commons BY-SA Lizenz](http://creativecommons.org/licenses/by-sa/4.0/) entwickelt.
Bei allen Einsendungen und Pull Requests gehen wir davon aus, dass sie unter der selben Lizenz eingesandt werden.
