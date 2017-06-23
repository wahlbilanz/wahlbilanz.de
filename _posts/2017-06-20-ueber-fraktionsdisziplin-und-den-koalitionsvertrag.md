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
---



{% include image.html align="alignright" url="/res/analyse/cluster-result/abstimmungscluster.pdf" img="/res/analyse/cluster-result/abstimmungscluster-preview.png" title="Übersicht über das Abstimmungsverhalten der einzelnen Parteien in der Legislatuerperiode 18 des Deutschen Bundestages" caption="Abbildung 1: Abstimmungsverhalten in der letzten Legislaturperiode" %}


Für das Projekt [DeinWal.de](https://deinwal.de) mussten wir die namentlichen Abstimmungen im Bundestag analysieren.
Welche Abstimmungen gab es überhaupt?
Welche Partei hat wie abgestimmt?
Kann man die Abstimmungen irgendwie gruppieren oder kategorisieren?
usw...


Um uns die Analyse einfacher zu machen haben wir die Daten natürlich auch visualisiert.
Das Ergebnis seht ihr in der großen Abbildung.
Diese Art der Visualisierung benutzen wir oft in der Bioinformatik um Expressionsmuster von Genen in verschiedenen Patienten zu untersuchen.
Die Grafik enthält sehr viele Informationen, daher ein kurzer Exkurs:



## Wie liest man die Heatmap?

Die Heatmap kann man sich als eine sehr große Tabelle vorstellen.
Jede Zeile der Tabelle steht für eine Abstimmung; am Ende der Zeile findet ihr auch die Abstimmung-ID:


{% include image.html align="alignleft" url="/img/2017-06-disziplin/zeile.png" img="/img/2017-06-disziplin/zeile.png" title="Erklärung: Heatmap-Zeile" caption="Abbildung 2: Jede Zeile in der Heatmap steht fuer eine Abstimmung" %}

In Abbildung 2 geht es also um die Abstimmung mit der ID `018-036-03`.
Diese ID setzt sich übrigens aus *Legislatuerperiode*-*Bundestagssitzung*-*Abstimmungsnummer* zusammen.
Im Beispiel geht es also um die Abstimmung Nummer 3 in Sitzung 36 des 18. Deutschen Bundestags!
Dabei ging es um [Gentechnikfreiheit im Pflanzenbau](/abstimmungen/018-036-03/) (siehe [wahlbilanz.de/abstimmungen/018-036-03/](/abstimmungen/018-036-03/)).

Jede Spalte in der Heatmap repräsentiert eine Partei.
Das sind, von links nach rechts: Die fraktionslose [Steinbach](https://de.wikipedia.org/wiki/Erika_Steinbach), [DIE LINKE](https://de.wikipedia.org/wiki/Linksfraktion), [Bündnis 90/Die Grünen](Bundestagsfraktion Bündnis 90/Die Grünen), [SPD](https://de.wikipedia.org/wiki/SPD-Bundestagsfraktion) und [CDU/CSU](https://de.wikipedia.org/wiki/CDU/CSU-Bundestagsfraktion).
In Abbildung 2 sind die Zellen der Fraktionslose, der SPD und der CDU also rot, während die Zellen von DIE LINKE und Bündnis 90/Die Grünen gelb sind.

Die Farbe einer Zellen entspricht dabei dem Abstimmungsergebnis der jeweiligen Partei bei einer bestimmten Abstimmung.
Gelb bedeutet "Nein", rot bedeutet "Ja".
Da die Parteien nicht immer geschlossen abstimmen gibt es verschiedene Orange-Töne dazwischen:

{% include image.html align="alignleft" url="/img/2017-06-disziplin/zelle.png" img="/img/2017-06-disziplin/zelle.png" title="Erklärung: Heatmap-Zellen und Verhältnis" caption="Abbildung 3: Die Farben einer Zelle entsprechen dem Abstimmungsverhältnis von *Nein* (rot) bis *Ja* (gelb)" %}

In Abbildung 3 waren sich die 3 Parteien also in [Abstimmung 018-209-02](/abstimmungen/018-209-02/) fast einig und haben alle eindeutig mit *Ja* gestimmt.
Bei der [Abstimmung 018-200-01](/abstimmungen/018-200-01/) gab es aber keinen Konsens: Die linke Zelle ist ziemlich rot (also dagegen), die mittlere Zelle ist orange (also eher untentschlossen), wohingegen die rechte Zelle wieder eindeutig gelb (also dafür) ist.
Das Abschätzen der Farben funktioniert natürlich nur grob.
Daher gibt es in jeder Spalte einen weiteren

Außerdem gibt es oben und an den Seiten ein Dendrogram.
D

In dem PDF gibt es oben links auch noch eine Farblegende.


## Was sieht man in der Heatmap?





## Methode

Für die Grafik habe ich ein kleines Script in der [Programmiersprache R](https://en.wikipedia.org/wiki/GNU_R) geschrieben, dass die Daten mit dem `heatmap.2` Tool aus der `gplots` Bibliothek analysiert und in einer Heatmap visualisert.
Die Daten kommen aus der [Datei `summary.table`](/res/abstimmungsliste/summary.table), die wir automatisch aus den Abstimmungsergebnissen generieren (siehe [integrate_new_results.py](/res/abstimmungsliste/integrate_new_results.py)).
Jeder Eintrag in der Tabelle entspricht dem Wert von *Ja* geteilt durch *Ja+Nein* -- **Enthaltungen werden also nicht berücksichtigt.**
Der gößte Teil des Scripts beschäftigt sich mit der Umbenennung der Parteinamen in eine gute, Menschen-lesbare Form:

{% highlight  R %}
{% cat res/analyse/cluster-result/cluster-abstimmungen.R %}
{% endhighlight %}

Da die fraktionslose Steinbach erst am 15. Januar 2017 aus der CDU ausgetreten ist, sind die Daten der linken Spalte in der Heatmap mit Vorsicht zu betrachten.
Nur Einträge ab [Abstimmung 018-212-01](/abstimmungen/018-212-01/) sind für der Spalte "Fraktionslos" relevant.


