---
title: "Obacht: Europawal!"
layout: post
published: true
date: 2019-04-08 13:48:40 +0200
categories:
  - Hintergrund
  - Analyse
tags:
  - Europa2019
authors:
  - binfalse
---


Ende Mai ist es wieder soweit: Die [MEPs](https://en.wikipedia.org/wiki/Member_of_the_European_Parliament) im europ&auml;ischen Parlament wollen gew&auml;hlt werden.
Und das passiert wie &uuml;blich im nat&uuml;rlichen Habitat des Europawals!
Also: Fernglaeser raus und sch&ouml;n die finger im Boot lassen.
Und nun zum Wetter...

### Spannung pur!

Die [Europawahl]() verspricht spannend zu werden!
In der aktuellen Legislaturperiode gab es einige interessante Entscheidungen, zum Beispiel ueber die Verwendung von Fluggastdaten, Neuzulassung von Glyphosat, verschiedene Handelsabkommen (CETA, TTIP, ..), Verbot von Einwegplastik und zuletzt die Reform des Urheberrechts...
Doch wie gut haben die Abgeordneten bei den offiziellen Abstimmungen eure Meinung vertreten?
Da das mal wieder gar nicht so leicht herauszufinden ist, hilft euch der Europawal :)





### Datenlage schwierig...

Wir kennen das ja schon von der Bundestagswahl: Die spannenden Daten sind verschlüsselt in komischen Datenformaten, siehe [erster Artikel](/2017/06/und-los/).

{% include image.html align="alignright" url="/img/2019-04-obacht-europawal/extract-2x1.pdf" img="/img/2019-04-obacht-europawal/extract-2x1.png" title="Gefangene Abstimmungsdaten..." caption="**Abbildung 1:** Gefangene Abstimmungsdaten..."   maxwidth='400px' %}

Für die Abstimmungen in der EU sieht die Datenlage leider noch einen Zacken schlimmer aus.
Ein offizielles Abstimmungsergebnis des EU-Parlaments ist in [Abbildung 1](/img/2019-04-obacht-europawal/extract-2x1.pdf) veranschaulicht:
Lange Listen mit Namen der Parlamentarier, inklusive voller Bandbreite an non-ASCII Zeichen.
Keine Zuordnung zu Ländern oder Parteien.
Lediglich die Zugehörigkeit zu den europäischen Koalitionen ist vorhanden..
Aber allein diese Datei zu finden ist eine anspruchsvolle Herausforderung!
Und dann besteht die Datei natürlich nicht nur aus dem Ergebnis einer Abstimmung - das Bild oben ist ein Extrakt aus einem [89-seitigem Dokument](http://www.europarl.europa.eu/sides/getDoc.do?pubRef=-//EP//NONSGML+PV+20141217+RES-RCV+DOC+PDF+V0//DE&language=DE), mit mehreren Entschliessungen, &Auml;nderungsantr&auml;gen, Entw&uuml;rfen, etc...
Und natürlich steht an diesem Abstimmungsergebnis nicht, um welche Abstimmung es überhaupt geht...
Zumindest nicht in einer menschenlesbaren Form.. Entschliessung `B8-0277/2014`... Aha, alles klar... ;-)




## Datenlage super!

Aber Gl&uuml;cklicherweise gibt es ja das Team von [*abgeordnetenwatch.de!*](https://www.abgeordnetenwatch.de/)
Dort wurde schon fleissig gesammelt und extrahiert und integriert...
Und es gibt eine [API](https://www.abgeordnetenwatch.de/api)! :)

Bei *abgeordnetenwatch.de* sind zwar nicht alle Abstimmungen verfügbar, aber mehr als 100 Abstimmungen sollten für einen EuropaWal genügen.
Also alles halb so schlimm.
Dank *abgeordnetenwatch.de* kann es nun doch einen EuropaWal geben.
[Genug zu tun](https://github.com/wahlbilanz/DeinWal.de/issues) gibt es aber trotzdem!




## Datenkunde

{% include image.html align="alignright" url="/res/2019-eu/analyse/cluster-votes/abstimmungscluster-from-individuals.pdf" img="/res/2019-eu/analyse/cluster-votes/abstimmungscluster-from-individuals.png" title="Heatmap des Abstimmungsverhaltens der einzelnen Parteien in der 8. Legislatuerperiode des Europäischen Parlaments" caption="**Abbildung 2:** Heatmap des Abstimmungsverhaltens der einzelnen Parteien in der 8. Legislatuerperiode des Europäischen Parlaments"  maxwidth='300px' %}

Natürlich haben wir uns zunächst ein Überblick über die Daten verschafft.
Dafür hat sich in der Vergangenheit immer ein Blick in die Heatmap gelohnt.
Und so auch hier, siehe [Abbildung 2!](/res/2019-eu/analyse/cluster-votes/abstimmungscluster-from-individuals.pdf")
(Wer die Karte nicht versteht, schaut am besten nochmal zu [*Wie liest man die Heatmap?*](/2017/06/ueber-fraktionsdisziplin-und-den-koalitionsvertrag/#wie-liest-man-die-heatmap) Die kryptischen Bezeichnungen für die Zeilen rechts entsprechen den [UUIDs](https://de.wikipedia.org/wiki/Universally_Unique_Identifier) der Abstimmungen bei *abgeordnetenwatch.de*)

Es wirkt jedenfalls wesentlich [spannender als bei der Bundestagswahl](/2017/06/ueber-fraktionsdisziplin-und-den-koalitionsvertrag/), oder?
Im EU-Parlament sind mehr Parteien vertreten und das Abstimmungsverhalten ist nicht so eine homogene Suppe!

Die hierarchischen Cluster über die Parteien (die Linien über der Heatmap) lassen auf drei Gruppen von sich ähnelnden Parteien schliessen:

* NPD, AfD und Die Blauen
* Die PARTEI, Die Linke, ÖDP, Piratenpartei und Die Grünen
* ALFA, Bündnis C, CDU/CSU, SPD, FDP und Freie Wähler

Wobei ich das mal gleich relativieren möchte!
Das hängt natürlich auch vom Clusteralgorithmus ab.
Es ist nämlich nicht so, dass die *SPD* ähnlicher zu *ALFA* (Distanz ist 7.15) als zu *Die Linke* (Distanz ist 4.62) ist!
Aber es zeigt eine gewisse Tendenz im Abstimmungsverhalten.


Am ähnlichsten sind sich ingesamt *Piratenpartei* und *Bündnis 90/Die Grünen* mit einer Distanz von 0.85.
Am unähnlichsten sind sich *SPD* und *AfD* mit einer Distanz von 9.17.


Die komplette Distanzmatrix der Parteien ist in [Abbildung 3](/res/2019-eu/analyse/cluster-votes/partydist-from-individuals.pdf) zu sehen.
Je grösser der Wert einer Zelle (bzw. je heller eine Zelle), desto unähnlicher sind sich die beiden Parteien.
Kleine Werte und rote Zellen bedeuten grosse Ähnlichkeit.

{% include image.html align='alignleft' url='/res/2019-eu/analyse/cluster-votes/partydist-from-individuals.pdf' img='/res/2019-eu/analyse/cluster-votes/partydist-from-individuals.png' title='Visualisierung der Distanzen zwischen den Parteien' caption='**Abbildung 3:** Visualisierung der Distanzen zwischen den Parteien. Kleine Werte in den Zellen beideutet kleine Distanz. Kleine Distanz bedeutet grosse Ähnlichkeit.' maxwidth='400px' %}




## Dev?

Wenn ihr gern entwicklt oder bastelt, solltet ihr mal in [das `res/2019-eu/wrangling/` Verzeichnis dieser Webseite](https://github.com/wahlbilanz/wahlbilanz.de/tree/master/res/2019-eu/wrangling/) schauen.
Dort gibt es ein paar Scripte, um zum Beispiel die Abstimmungsergebnisse für eine UUID zu bekommen; oder um die UUID für eine Seite bei *abgeordnetenwatch.de* herauszufinden.


## Der EuropaWal kann jeden moment auftauchen!

Ja.... Und dank der Datenaufbereitung von *abgeordnetenwatch.de* kann der EuropaWal nun bald an den Start gehen, um die wählende Bevölkerung über vergangene Entscheidungen im Europaparlament aufzuklären!
Seid gespannt und halten Augen und Ohren offen und guckt bei [DeinWal.de](https://deinwal.de/) vorbei :)
