---
title: "Über die Ähnlichkeit der Parteien"
layout: post
published: true
date: 2018-05-12 21:58:51 +0200
categories:
  - Hintergrund
  - Analyse
tags:
  - Kiel2018
authors:
  - binfalse
---




Wir wurden gebeten, die *N&auml;he der politischen Parteien* zu analysieren, die bei den [Kommunalwahlen 2018 in Kiel](https://de.wikipedia.org/wiki/Ergebnisse_der_Kommunalwahlen_in_Kiel) angetreten sind.
Speziell geht es um die Antworten der Parteien [SPD](https://de.wikipedia.org/wiki/Sozialdemokratische_Partei_Deutschlands), [CDU](https://de.wikipedia.org/wiki/Christlich_Demokratische_Union_Deutschlands), [Die Grünen](https://de.wikipedia.org/wiki/B%C3%BCndnis_90/Die_Gr%C3%BCnen), [Die Linke](https://de.wikipedia.org/wiki/Die_Linke), [FPD](https://de.wikipedia.org/wiki/Freie_Demokratische_Partei), [AfD](https://de.wikipedia.org/wiki/Alternative_f%C3%BCr_Deutschland), [SSW](https://de.wikipedia.org/wiki/S%C3%BCdschleswigscher_W%C3%A4hlerverband), [Die Partei](https://de.wikipedia.org/wiki/Partei_f%C3%BCr_Arbeit,_Rechtsstaat,_Tierschutz,_Elitenf%C3%B6rderung_und_basisdemokratische_Initiative), und [Piratenpartei](https://de.wikipedia.org/wiki/Piratenpartei_Deutschland) auf die 30 Fragen des Lokal-O-Mat.
Die [Ergebnisse der Wahl](https://www.kiel.de/de/politik_verwaltung/meldung.php?id=78551) stehen mittlerweile fest, die Parteien zu vergleichen ist aber trotzdem spannend! :)


## Parteien und Themen analysieren

{% include image.html align="alignright" url="/res/analyse/kw-kiel-2018/clusteranalysis/abstimmungscluster.pdf" img="/res/analyse/kw-kiel-2018/clusteranalysis/abstimmungscluster.png" title="Übersicht über das Abstimmungsverhalten der einzelnen Parteien zur Kommunalwahl in Kiel" caption="**Abbildung 1:** Abstimmungsverhalten zur Kommunalwahl in Kiel" %}

Analog zur Analyse [*&uuml;ber Fraktionsdisziplin und den Koalitionsvertrag*](https://wahlbilanz.de/2017/06/ueber-fraktionsdisziplin-und-den-koalitionsvertrag/) habe ich die Antwortmatrix in einer [Heatmap](https://de.wikipedia.org/wiki/Heatmap) visualisiert.
Die Methode zu adaptieren war einfach, hier ist das neue R-Script:


{% highlight  R %}
{% cat res/analyse/kw-kiel-2018/clusteranalysis/cluster.R %}
{% endhighlight %}

Das Ergebniss seht ihr in [Abbildung 1](/res/analyse/kw-kiel-2018/clusteranalysis/abstimmungscluster.pdf).
Die Zeilen in der Heatmap entsprechen den Themengebieten (siehe Beschriftung rechts am Ende jeder Zeile).
Die Spalten repr&auml;sentieren die Parteien (siehe Parteinamen unter der Heatmap).
Die Farbe in einer Zelle der Heatmap zeigt, wie die jeweilige Partei bei dem entsprechenden Themengebiet gestimmt hat:
*Gelb* bedeutet *Ja*, *Orange* bedeutet *Neutral* und *Rot* bedeutet *Nein*.
Zur *Unterbringung von Gefl&uuml;chteten* (erste Zeile in der Heatmap) hat die *AfD* beispielsweise mit *Nein* gestimmt, w&auml;hrend alle anderen Parteien mit *Ja* gestimmt haben.

Die Methode gruppiert auch Parteien und Themen nach &auml;hnlichen Mustern, was in den [Dendrogrammen](https://de.wikipedia.org/wiki/Hierarchische_Clusteranalyse#Dendrogramm) links und oben zu sehen ist.
Je k&uuml;rzer der Pfad, desto &auml;hnlicher sind sich die Parteien oder Abstimmungsergebnisse.
Man sieht beispielsweise, dass die Distanz zwischen *Die Gr&uuml;nen* und *Die Linke* sehr klein ist (die beiden Parteien zeigen ein &auml;hnliches Abstimmungsverhalten), w&auml;hrend die *AfD* sehr weit weg von den anderen Parteien ist.

Aus der Heatmap kann man auch ablesen, wie kontrovers ein Thema ist -- oder wie sehr es uns hilft die Parteien zu unterscheiden.
W&auml;hrend die Varianz in den Antworten zu *Pavillons am Alten Markt* oder zur *Unterbringung von Geflüchteten* sehr klein ist (die Parteien sind sich fast einig), ist die Varianz zum *Flughafen Kiel Holtenau* oder zum *Messe- und Kongresszentrum* sehr hoch (die Antworten der Parteien unterscheiden sich stark).


Die Heatmap ist komplex und bietet viele detaillierte Informationen in einer einzelnen Abbildung -- zumindest f&uuml;r das geschulte Auge.
Aus dem Feedback zur Bundestagswahl haben wir jedoch gelernt, dass diese Art der Visualisierung sehr schwer zu verstehen ist, wenn man nicht regelm&auml;ssig mit Heatmaps in Kontakt kommt.
Unser Ziel ist es also, eine Grafik mit kleinerer Informationsdichte zu entwickeln, die einfacher zu lesen ist.



## Parteienkreise visualisieren die &Auml;hnlichkeit von Parteipositionen

Zusammen mit einigen Kollegen am [Lehrstuhl f&uuml;r Systembiologie und Bioinformatik](https://www.sbi.uni-rostock.de/) an der [Universit&auml;t Rostock](https://www.uni-rostock.de/) haben wir die Parteienkreise entwickelt.
Ein Parteienkreis zeigt, wie stark die Position einer Partei mit den Positionen der anderen Parteien &uuml;bereinstimmt.
Abbildung 3 pr&auml;sentiert ein Beispiel f&uuml;r die *SSW* in Kiel:

{% include image.html align="alignleft" url="/res/analyse/kw-kiel-2018/pies/pie-ssw.svg" img="/res/analyse/kw-kiel-2018/pies/pie-ssw-demo.png" title="Parteienkreis der SSW" caption="**Abbildung 2:** Parteienkreis der SSW" %}


Der &auml;u&szlig;ere blaue Kreis steht f&uuml;r die Position der *SSW* zu den 30 Themengebieten des Lokal-O-Mat.
Die bunten Kreissektoren im Inneren repr&auml;sentieren die anderen Parteien.
Der Radius eines Kreissektors entspricht dabei der Anzahl an &uuml;bereinstimmenden Antworten der beiden Parteien.
Es gilt also: Je gr&ouml;sser der Radius des Kreissektors, desto &auml;nlicher sind sich die Parteipositionen in den 30 Themen.
An den Grenzen der Kreissektoren sind Skalen angedeutet, an denen man die Anzahl der &Uuml;bereinstimmungen ablesen kann.
Die horizontale Achse nach rechts ist zudem beschriftet.
In dem Parteienkreis f&uuml;r die *SSW* sieht man also, dass die *CDU* 12-mal und *Die Gr&uuml;nen* 17-mal so gestimmt haben wie die *SSW*.
Es ist auch ersichtlich, dass *Die Partei* und *Die Linke* die gr&ouml;ssten &Uuml;bereinstimmungen haben: Beide haben 21-mal genau wie die *SSW* abgestimmt.
Auf der anderen Seite hat die *SSW* die kleinste Gemeinsamkeit mit der *AfD*:
Die beiden Parteien haben in nur 11 F&auml;llen gleich gestimmt.  
H&auml;tte eine Partei alle Fragen genau wie die *SSW* beantwortet, dann w&uuml;rde der entsprechende Kreissektor den &auml;u&szlig;eren Kreis ber&uuml;hren.


Der Parteienkreis zeigt also die &Auml;hnlichkeit einer Partei zu den anderen Parteien.
Hier folgen nun die Kreise f&uuml;r alle Parteien zur Kommunalwahl in Kiel.
&Uuml;ber die Links unter den Kreisen gelangt ihr zu hochaufl&ouml;senden Versionen in [PNG](https://de.wikipedia.org/wiki/Portable_Network_Graphics) und [SVG](https://de.wikipedia.org/wiki/Scalable_Vector_Graphics) Format.


{% include image.html align="floatleft" url="/res/analyse/kw-kiel-2018/pies/pie-afd.svg" img="/res/analyse/kw-kiel-2018/pies/pie-afd-preview.png" title="AfD" caption="AfD ([PNG](/res/analyse/kw-kiel-2018/pies/pie-afd.png)/[SVG](/res/analyse/kw-kiel-2018/pies/pie-afd.svg))" %}
{% include image.html align="floatleft" url="/res/analyse/kw-kiel-2018/pies/pie-cdu.svg" img="/res/analyse/kw-kiel-2018/pies/pie-cdu-preview.png" title="CDU" caption="CDU ([PNG](/res/analyse/kw-kiel-2018/pies/pie-cdu.png)/[SVG](/res/analyse/kw-kiel-2018/pies/pie-cdu.svg))" %}
{% include image.html align="floatleft" url="/res/analyse/kw-kiel-2018/pies/pie-die-partei.svg" img="/res/analyse/kw-kiel-2018/pies/pie-die-partei-preview.png" title="Die Partei" caption="Die Partei ([PNG](/res/analyse/kw-kiel-2018/pies/pie-die-partei.png)/[SVG](/res/analyse/kw-kiel-2018/pies/pie-die-partei.svg))" %}
{% include image.html align="floatleft" url="/res/analyse/kw-kiel-2018/pies/pie-fdp.svg" img="/res/analyse/kw-kiel-2018/pies/pie-fdp-preview.png" title="FDP" caption="FDP ([PNG](/res/analyse/kw-kiel-2018/pies/pie-fdp.png)/[SVG](/res/analyse/kw-kiel-2018/pies/pie-fdp.svg))" %}
{% include image.html align="floatleft" url="/res/analyse/kw-kiel-2018/pies/pie-gruene.svg" img="/res/analyse/kw-kiel-2018/pies/pie-gruene-preview.png" title="Die Grünen" caption="Die Grünen ([PNG](/res/analyse/kw-kiel-2018/pies/pie-gruene.png)/[SVG](/res/analyse/kw-kiel-2018/pies/pie-gruene.svg))" %}
{% include image.html align="floatleft" url="/res/analyse/kw-kiel-2018/pies/pie-linke.svg" img="/res/analyse/kw-kiel-2018/pies/pie-linke-preview.png" title="Die Linke" caption="Die Linke ([PNG](/res/analyse/kw-kiel-2018/pies/pie-linke.png)/[SVG](/res/analyse/kw-kiel-2018/pies/pie-linke.svg))" %}
{% include image.html align="floatleft" url="/res/analyse/kw-kiel-2018/pies/pie-piraten.svg" img="/res/analyse/kw-kiel-2018/pies/pie-piraten-preview.png" title="Piratenpartei" caption="Piratenpartei ([PNG](/res/analyse/kw-kiel-2018/pies/pie-piraten.png)/[SVG](/res/analyse/kw-kiel-2018/pies/pie-piraten.svg))" %}
{% include image.html align="floatleft" url="/res/analyse/kw-kiel-2018/pies/pie-spd.svg" img="/res/analyse/kw-kiel-2018/pies/pie-spd-preview.png" title="SPD" caption="SPD ([PNG](/res/analyse/kw-kiel-2018/pies/pie-spd.png)/[SVG](/res/analyse/kw-kiel-2018/pies/pie-spd.svg))" %}
{% include image.html align="floatleft" url="/res/analyse/kw-kiel-2018/pies/pie-ssw.svg" img="/res/analyse/kw-kiel-2018/pies/pie-ssw-preview.png" title="SSW" caption="SSW ([PNG](/res/analyse/kw-kiel-2018/pies/pie-ssw.png)/[SVG](/res/analyse/kw-kiel-2018/pies/pie-ssw.svg))" %}

<div style="clear: both;"></div>



Ihr k&ouml;nnt die Kreise gern unter der [Creative Commons BY-SA 4.0 Lizenz](http://creativecommons.org/licenses/by-sa/4.0/) f&uuml;r eigene Abbildungen und Kompositionen verwenden.
Bei der Entwicklung der Abbildung haben die Datenwissenschaftler 
[Patrick Schopohl](https://www.sbi.uni-rostock.de/team/detail/dr-patrick-schopohl),
[Saptarshi Bej](https://www.sbi.uni-rostock.de/team/detail/saptarshi-bej),
[Tom Gebhardt](https://www.sbi.uni-rostock.de/team/detail/tom-gebhardt),
[Markus Wolfien](https://www.sbi.uni-rostock.de/team/detail/markus-wolfien),
[Ali Salehzadeh-Yazdi](https://www.sbi.uni-rostock.de/team/detail/ali-salehzadeh-yazdi) und 
[Olaf Wolkenhauer](https://www.sbi.uni-rostock.de/team/detail/prof-olaf-wolkenhauer)
maßgeblich mitgewirkt.
Zusammen haben wir auch die folgende Collage entwickelt:



{% include image.html align="alignleft" url="/res/analyse/kw-kiel-2018/pies/parteivergleich.svg" img="/res/analyse/kw-kiel-2018/pies/parteivergleich-preview.png" title="Parteienkreise zur Kommunalwahl in Kiel 2018" caption="**Abbildung 3:** Parteienkreise zur Kommunalwahl in Kiel 2018 ([PNG](/res/analyse/kw-kiel-2018/pies/parteivergleich.png)/[SVG](/res/analyse/kw-kiel-2018/pies/parteivergleich.svg))" %}









## Disclaimer

Ich habe mich mit der Kieler Politik nicht besch&auml;ftigt und kann daher &uuml;ber die konkreten Inhalte der Themengebiete nur spekulieren, aber die Politik soll hier auch eine eher untergeordnete Rolle spielen.












