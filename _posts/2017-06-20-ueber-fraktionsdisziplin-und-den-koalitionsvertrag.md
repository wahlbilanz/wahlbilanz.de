---
title: "Über Fraktionsdisziplin und den Koalitionsvertrag"
layout: post
published: true
date: 2017-06-20 16:27:35 +0200
categories:
  - Hintergrund
  - Analyse
tags:
  - Koalition
  - Freie Wahl
  - Disziplin
  - Analyse
  - R
authors:
  - binfalse
---



{% include image.html align="alignright" url="/res/analyse/cluster-result/abstimmungscluster.pdf" img="/img/2017-06-disziplin/abstimmungscluster-preview.jpg" title="Übersicht über das Abstimmungsverhalten der einzelnen Parteien in der Legislatuerperiode 18 des Deutschen Bundestages" caption="**Abbildung 1:** Abstimmungsverhalten in der letzten Legislaturperiode" %}


Für das Projekt [DeinWal.de](https://deinwal.de) haben wir alle namentlichen Abstimmungen im Bundestag analysiert.
Welche Abstimmungen gab es überhaupt?
Welche Partei hat wie abgestimmt?
Kann man die Abstimmungen irgendwie gruppieren oder kategorisieren?
usw...


Um uns die Analyse einfacher zu machen wurden die Daten natürlich auch visualisiert.
Eines der Ergebnisse seht ihr in [Abbildung 1](/res/analyse/cluster-result/abstimmungscluster.pdf).
Diese Art der Visualisierung benutzen wir oft in der Bioinformatik um Expressionsmuster von Genen in verschiedenen Patienten zu untersuchen.
Die Grafik zeigt eine Heatmap und enthält sehr viele Informationen, daher ein kurzer Exkurs:



## Wie liest man die Heatmap?

Die Heatmap kann man sich als eine sehr große Tabelle vorstellen.
Jede Zeile der Tabelle steht für eine Abstimmung; am Ende der Zeile findet ihr auch die Abstimmungs-ID:


{% include image.html align="alignleft" url="/img/2017-06-disziplin/zeile.png" img="/img/2017-06-disziplin/zeile.png" title="Erklärung: Heatmap-Zeile" caption="**Abbildung 2:** Jede Zeile in der Heatmap steht fuer eine Abstimmung" %}

In Abbildung 2 geht es also um die Abstimmung mit der ID `018-036-03`.
Diese ID setzt sich übrigens aus *Legislaturperiode*, *Bundestagssitzung* und *Abstimmungsnummer* zusammen.
Im Beispiel handelt es sich also um die Abstimmung Nummer 3 in Sitzung 36 des 18. Deutschen Bundestags!
Dabei ging es um [Gentechnikfreiheit im Pflanzenbau](/abstimmungen/018-036-03/) (siehe [wahlbilanz.de/abstimmungen/018-036-03/](/abstimmungen/018-036-03/)).

Jede Spalte in der Heatmap repräsentiert eine Partei.
Das sind, von links nach rechts: [DIE LINKE](https://de.wikipedia.org/wiki/Linksfraktion), [Bündnis 90/Die Grünen](https://de.wikipedia.org/wiki/Bundestagsfraktion_B%C3%BCndnis_90/Die_Gr%C3%BCnen), die fraktionslose [Steinbach](https://de.wikipedia.org/wiki/Erika_Steinbach), [SPD](https://de.wikipedia.org/wiki/SPD-Bundestagsfraktion) und [CDU/CSU](https://de.wikipedia.org/wiki/CDU/CSU-Bundestagsfraktion).
In Abbildung 2 sind die Zellen von DIE LINKE und Bündnis 90/Die Grünen also gelb, die Zelle der Fraktionslosen ist grau, und die Zellen der SPD und der CDU/CSU sind rot.

Die Farbe einer Zelle entspricht dabei dem Abstimmungsergebnis der jeweiligen Partei bei einer bestimmten Abstimmung.
Es gibt drei Grundfarben:

* Gelb bedeutet "JA".
* Rot bedeutet "Nein".
* Grau bedeutet, dass keine Daten vorliegen, z.B. weil sich die Partei bei dieser Abstimmung komplett enthalten hat oder noch nicht existierte (Frau Steinbach war bis zum 15. Januar 2017 Mitlgied der CDU).

Da die Parteien nicht immer geschlossen abstimmen gibt es zudem verschiedene Orange-Töne zwischen rot und gelb:

{% include image.html align="alignleft" url="/img/2017-06-disziplin/zelle.png" img="/img/2017-06-disziplin/zelle.png" title="Erklärung: Heatmap-Zellen und Verhältnis" caption="**Abbildung 3:** Die Farben einer Zelle entsprechen dem Abstimmungsverhältnis von *Nein* (rot) bis *Ja* (gelb)" %}

In Abbildung 3 waren sich die Parteien in den hinteren Spalten also bei der [Abstimmung 018-237-05](/abstimmungen/018-237-05/) fast einig und haben alle eindeutig mit *Ja* (Gelb) gestimmt während die Partei in der ersten Spalte geschlossen mit *Nein* (Rot) stimmte.
Bei den Abstimmungen [018-200-01](/abstimmungen/018-200-01/), [018-198-03](/abstimmungen/018-198-03/) und [018-134-03](/abstimmungen/018-134-03/) war das Ergebnis aber nicht so klar:

* Die Partei in der ersten Spalte hat beispielsweise immer dagegen gestimmt (alles Rot).
* Zur Partei in der zweiten Spalte gibt es gar keine Daten (Grau).
* Die Partei in der dritten Spalte zeigt deutlich Uneinigkeiten. Während sie bei [018-200-01](/abstimmungen/018-200-01/) noch knapp dafür war (helleres Orange) hat sie bei [018-198-03](/abstimmungen/018-198-03/) und [018-134-03](/abstimmungen/018-134-03/) knapp dagegen gestimmt (dunkleres Orange).
* Bei der vierten Partei in der rechten Spalte zeigen sich auch Uneinigkeiten, die Entscheidungen fielen aber eindeutig mit *Ja* aus (sehr helles Orange).

Das Abschätzen der Farben funktioniert natürlich nur grob.
Daher gibt es in jeder Spalte zwei Linien, die den Wert ein bisschen genauer abbilden.
Die gestrichelte Linie in der Mitte jeder Spalte gibt jeweils an wo 50% ist (*Ja*=*Nein* wäre).
Die durchgezogene Linie gibt Aufschluss über das genaue Abstimmungsverhältnis.
Ist sie ganz links in der Spalte bedeutet das 100% dagegen, ist sie ganz rechts heißt das, dass die Partei 100% dafür war.
Wenn wir uns jetzt nochmal Abbildung 3 angucken, sehen wir, dass die durchgezogene Linie der dritten Partei bei Abstimmung [018-200-01](/abstimmungen/018-200-01/) knapp rechts von der gestrichelten Linie ist (knappe Mehrheit für *Ja*) aber bei den Abstimmungen [018-198-03](/abstimmungen/018-198-03/) und [018-134-03](/abstimmungen/018-134-03/) knapp links von der gestrichelten Linie ist (also knappe Mehrheit für *Nein*).

Zu guter Letzt gibt es oben und auf der linken Seite je ein [Dendrogram](https://de.wikipedia.org/wiki/Hierarchische_Clusteranalyse#Dendrogramm).
An dem Dendrogram kann man die Ähnlichkeiten der Parteien/Abstimmungsergebnisse ablesen.
Je kürzer der Pfad zwischen zwei Spalten/Zeilen, desto ähnlicher sind sie sich.


Mit einem [Klick auf Abbildung 1](/res/analyse/cluster-result/abstimmungscluster.pdf) könnt ihr die Heatmap in höherer Auflösung als PDF herunter laden!


## Was sieht man in der Heatmap?


{% include image.html align="alignright" url="/res/analyse/cluster-result/abstimmungscluster.pdf" img="/img/2017-06-disziplin/abstimmungscluster-preview.jpg" title="Übersicht über das Abstimmungsverhalten der einzelnen Parteien in der Legislatuerperiode 18 des Deutschen Bundestages" caption="**Abbildung 1:** Abstimmungsverhalten in der letzten Legislaturperiode" %}

Für eine leichtere Lesbarkeit habe ich die Heatmap aus [Abbildung 1](/res/analyse/cluster-result/abstimmungscluster.pdf) hier unten einfach nochmal eingebunden.

Zunächst fällt vielleicht auf, das die Spalte der Fraktionslosen größtenteils Grau ist.
Das ist leicht zu erklären: Frau Steinbach ist erst am 15. Januar 2017 aus der CDU ausgetreten, d.h. vor der [Abstimmung 018-212-01](/abstimmungen/018-212-01/) gab es keine Fraktionslose und damit auch keine Daten für diese Spalte.
Danach hat Frau Steinbach aber scheinbar weiter im Sinne der CDU/CSU abgestimmt, bis auf [Abstimmung 018-237-13](/abstimmungen/018-237-13/).

Daher sind die Fraktionslose und CDU/CSU auch sehr ähnlich, wie man im Dendrogram oben sieht.
Nur der Weg zwischen CDU/CSU und SPD ist kürzer.
Was wiederrum bedeutet, dass diese beiden Parteien oft gleich abgestimmt haben.
Das ist sicher dem [Koalitionsvertrag](https://de.wikipedia.org/wiki/Koalitionsvertrag_der_18._Wahlperiode_des_Bundestages) geschuldet, den die Fraktionen zu Beginn der Legislatuerperiode ausgehandelt haben und an den sie sich jetzt halten (müssen).


DIE LINKE und Bündnis 90/Die Grünen sind sich nicht so ähnlich; sie haben wahrscheinlich auch nicht solch einen Vertrag miteinander.
Sie sind sich dennoch ähnlicher als, beispielsweise, DIE LINKE und SPD.
Während es bei Bündnis 90/Die Grünen noch leicht fällt Abstimmungsergebnisse im Sinne der großen Koalition zu finden (~50), ist die Schnittmenge zwischen DIE LINKE und große Koalition eher überschaubar (~10).



Es gibt in der gesamten Heatmap auffallend wenig Orange!
Das bedeutet, dass die Fraktionen in der Regel immer geschlossen abgestimmt haben.
Dieses Prinzip nennt man [Fraktionsdisziplin oder Fraktionszwang](https://de.wikipedia.org/wiki/Fraktionsdisziplin).
Ein Faktor für diesen Effekt ist wahrscheinlich der großen Druck und der Wettbewerb um Listenplätze innerhalb einer Partei.
Der Effekt entsteht aber sicher auch, weil natürlich nicht jeder Abgeordnete ein Sachverständiger für alle behandelten Themen ist.
Er muss sich auf die Meinung seiner Parteikollegen aus speziellen Gremien und Ausschüssen verlassen.
So kommt es nur selten vor, dass ein Abgeordneter gegen die Meinung seiner Partei stimmt.








## Methode

Für die Grafik habe ich ein kleines Script in der [Programmiersprache R](https://en.wikipedia.org/wiki/GNU_R) geschrieben, dass die Daten mit dem [`heatmap.2` Tool](https://www.rdocumentation.org/packages/gplots/versions/3.0.1/topics/heatmap.2) aus der [`gplots` Bibliothek](https://cran.r-project.org/web/packages/gplots/index.html) analysiert und in einer Heatmap visualisert.
Die Daten kommen aus der [Datei `summary.table`](/res/abstimmungsliste/summary.table), die wir automatisch aus den Abstimmungsergebnissen generieren (siehe [integrate_new_results.py](/res/abstimmungsliste/integrate_new_results.py)).
Jeder Eintrag in der Tabelle entspricht dem Wert von *Ja* geteilt durch *Ja+Nein* -- **Enthaltungen werden also nicht berücksichtigt.**
Der größte Teil des Scripts beschäftigt sich mit der Umbenennung der Parteinamen in eine gute, Menschen-lesbare Form:

{% highlight  R %}
{% cat res/analyse/cluster-result/cluster-abstimmungen.R %}
{% endhighlight %}

