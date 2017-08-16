---
title: "Wer schwänzt am meisten?"
layout: post
published: true
date: 2017-07-28 20:34:04 +0200
categories:
  - uncategorized
tags:
  - untagged
---

Na, was denkt ihr: Welche Partei schwänzt am öftesten die namentlichen Abstimmungen!?

Dank der Computer-lesbaren Abstimmungsdateien im Wahlbilanz-Projekt (siehe [Erläuterungen auf Github](https://github.com/wahlbilanz/wahlbilanz.de/tree/master/abstimmungen#readme)) können wir das relativ einfach herausfinden.
Also gucken wir doch mal nach!
Mit einem sehr einfachen Script konnte ich folgendes Balkendiagram generieren:


{% include image.html url='/res/analyse/schwaenzer/schwaenzer-bars-absolut.pdf' img='/img/schwaenzer/schwaenzer-bars-absolut.jpg' title='Wer schwänzt am meisten?' caption='Wer schwänzt am meisten?' %}


**Boar was!?
CDU/CDU haben weit mehr als 4000 mal geschwänzt!?!?**

Wer das jetzt denkt sollte wirklich kritischer mit solchen Artikeln umgehen!
Das ist doch bisher nur ein "Bild".
Wo kommen denn die Daten her?

## Die Skripte

Ich will hier gar nicht so viele technische Details bringen.
Um die Daten zu erzeugen habe ich ein [Python-Programm](https://github.com/wahlbilanz/wahlbilanz.de/blob/master/abstimmungen/applications/schwaenzer.py) geschrieben, das mit Hilfe des [Abstimmungsparsers](https://github.com/wahlbilanz/wahlbilanz.de/blob/master/abstimmungen/abstimmungsparser.py) die Abstimmungen des Bundestags analysiert: Es trägt für jede Abstimmung die Zahl der *nicht abgegebenen* Stimmen pro Bundestagspartei zusammen und gibt [das Ergbnis in JSON-Format](https://github.com/wahlbilanz/wahlbilanz.de/blob/master/res/analyse/schwaenzer/data.json) aus.
Ein zweites [R-Programm](https://github.com/wahlbilanz/wahlbilanz.de/blob/master/res/analyse/schwaenzer/visualiser.R) liest das Resultat und generiert Grafiken.







Heraus kommt folgendes Ergebnis:

| Partei | Absolut geschwänzt | Relativ geschwänzt | Anzahl teilgenommene Abstimmungen |
| ------ | ------------------ | ------------------ | --------------------------------- |
| Bündnis 90/Die Grünen | 1189 | 18.87 | 212|
| CDU/CSU | 4635 | 14.94 | 212 |
| SPD | 3397 | 17.60 | 212 |
| Die Linke | 1925 | 30.08 | 212 |
| Fraktionslos | 13 | 13.00 | 37 |




nicht bei einer abstimmung zu sein heisst natuerlich nicht, dass die abgeordneten faul sind.
sind viel unterwegs und haben andere sachen zu tun...




{% include image.html align='alignright' url='/assets/media/pics/2017/' img='/assets/media/pics/2017/' title='ALT' caption='CAPTION' maxwidth='300px' %}

{% highlight bash %}
some code
{% endhighlight %}

*italics*

**strong**

[link](url)


