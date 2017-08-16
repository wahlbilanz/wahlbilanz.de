---
title: "Wer schwänzt am meisten?"
layout: post
published: true
date: 2017-07-28 20:34:04 +0200
categories:
  - Hintergrund
  - Analyse
tags:
  - Disziplin
  - Analyse
  - R
  - Python
authors:
  - binfalse
---

Na, was denkt ihr: Welche Partei schwänzt am öftesten die namentlichen Abstimmungen!?

Dank der Computer-lesbaren Abstimmungsdateien im Wahlbilanz-Projekt (siehe [Erläuterungen auf Github](https://github.com/wahlbilanz/wahlbilanz.de/tree/master/abstimmungen#readme)) können wir das relativ einfach herausfinden.
Also gucken wir doch mal nach!
Mit einem sehr einfachen Script konnte ich folgendes Balkendiagram generieren:


{% include image.html url='/res/analyse/schwaenzer/schwaenzer-bars-absolut.pdf' img='/img/schwaenzer/schwaenzer-bars-absolut.png' title='Wer schwänzt am meisten?' caption='Wer schwänzt am meisten?' %}


**Boar was!?
CDU/CDU haben weit mehr als 4000 mal geschwänzt!?!?**

Wer das jetzt denkt sollte wirklich kritischer mit solchen Artikeln umgehen!
Das ist doch bisher nur ein "Bild".
Wo kommen denn die Daten her?

## Die Skripte

Ich will hier gar nicht so viele technische Details bringen.
Um die Daten zu erzeugen habe ich ein [Python-Programm](https://github.com/wahlbilanz/wahlbilanz.de/blob/master/abstimmungen/applications/schwaenzer.py) geschrieben, das mit Hilfe des [Abstimmungsparsers](https://github.com/wahlbilanz/wahlbilanz.de/blob/master/abstimmungen/abstimmungsparser.py) die Abstimmungen des Bundestags analysiert: Es trägt für jede Abstimmung die Zahl der *nicht abgegebenen* Stimmen pro Bundestagspartei zusammen und gibt [das Ergbnis in JSON-Format](https://github.com/wahlbilanz/wahlbilanz.de/blob/master/res/analyse/schwaenzer/data.json) aus.
Ein zweites [R-Programm](https://github.com/wahlbilanz/wahlbilanz.de/blob/master/res/analyse/schwaenzer/visualiser.R) liest das Resultat und generiert Grafiken.


## Die Daten

Genug technischer Details -- so sehen die Daten aus:


| Partei | Absolut geschwänzt | Relativ geschwänzt | Anzahl teilgenommene Abstimmungen |
| ------ | ------------------:| ------------------:| ---------------------------------:|
| CDU/CSU | 4635 | 14.94 | 212 |
| SPD | 3397 | 17.60 | 212 |
| Die Linke | 1925 | 30.08 | 212 |
| Bündnis 90/Die Grünen | 1189 | 18.87 | 212|
| Fraktionslos | 13 | 13.00 | 37 |


Die Spalte *Absolut geschwänzt* ist eindeutig: Die Abgeordneten von CDU/CSU haben wirklich 4635 Stimmen bei namentlichen Abstimmungen nicht abgegebenen!
Damit liegen CDU/CSU ziemlich weit vor der SPD.
Am fleißigsten waren scheinbar die Abgeordneten von Bündnis 90/Die Grünen: sie haben in den letzten 4 Jahren nur 1189 Stimmen nicht abgegeben.
Die Fraktionslose lassen wir für den Moment einfach außer Betracht, da sie als Fraktionslose überhaupt an weit weniger Abstimmungen teilgenommen hat.


Die kritischeren Denker unter euch sehen aber sicher schon die Ungereimtheit:
Die Fraktionen sind natürlich alle unterschiedlich groß!
Beispielsweise haben bei der Abstimmung zur [Abschaffung der sachgrundlosen Befristung](https://wahlbilanz.de/abstimmungen/018-241-01/) 50 Abgeordnete der CDU/CSU und 40 Abgeordnete der SPD nicht teilgenommen.
In der CDU/CSU haben aber auch 259 Abgeordnete abgestimmt, während bei der SPD "nur" 153 Abgeordnete ihre Stimme abgaben.
Das heißt, die Wahlbeteiligung war hier bei der CDU/CSU mit 83,82% höher als bei der SPD mit 79,27%.
Die absoluten Zahlen sind also nicht geeignet um eine Solche Frage zu beantworten.



## Also relativ gesehen...?

Aus der Tabelle oben könnt ihr die relativen Ergebnisse schon ablesen.
Da sich die Werte in einer Grafik aber leichter vergleichen lassen:

{% include image.html url='/res/analyse/schwaenzer/schwaenzer-bars-relativ.pdf' img='/img/schwaenzer/schwaenzer-bars-relativ.png' title='Wer schwänzt am meisten?' caption='Wer schwänzt am meisten?' %}


Ja, also relativ gesehen hatte Einstein wohl recht: Da sieht die Sache plötzlich ganz anders aus.

Verglichen mit der Zahl an abgegeben Stimmen fallen die 4635 nicht abgegebenen Stimmen der CDU/CSU fast gar nicht mehr auf.
Nun sehen die Abgeordneten der CDU/CSU mit im Schnitt nur 14.94% versäumten Stimmen sogar richtig fleißig aus!
Knapp gefolgt von der SPD, die im Durchschnitt 17.60% der Stimmen nicht wahr genommen hat.

Aber was ist denn da mit den Linken los?
Im Bild oben noch ganz unscheinbar, ergibt sich nun ein völlig anderes Bild.
Mit durchschnittlich 30.08% nicht abgegebenen Stimmen sticht Die Linke nun ziemlich heraus.




## Disclaimer

Dieser Artikel soll niemanden an den Pranger stellen.
Ich möchte eher zur Aufmerksamkeit aufrufen.
Wie oben gesehen können Daten immer verschieden interpretiert werden können -- je nachdem was man gerade aussagen will.
Gerade bei der schnelllebigen Medienlandschaft sollte man umso kritischer sein und nicht alles, was vorbeigescrollt kommt, glauben.
Und ich wollte natürlich die Daten in dieser Webseite und [dem zugehörigen Projekt auf GitHub](https://github.com/wahlbilanz/wahlbilanz.de) bewerben.. :P


**Dieses Thema ist ehrlich gesagt auch vollkommener Quatsch!**
Wenn ein Abgeordneter bei einer Abstimmung nicht dabei ist, ist das nicht zwangsweise auf "Faulheit" zurückzuführen (^^).
Vielleicht eher im Gegenteil: Wer bei unkontroversen/klaren Abstimmungen im Plenum rumsitzt arbeitet nicht an wichtigen anderen Aufgaben.
Abgeordnete sind sicher auch viel unterwegs und können oft aus beruflichen oder gesundheitlichen Günden nicht an den Abstimmungen teilnehmen.



Ich werde euch jetzt auch nicht sagen **wer der Abgeordnete ist, der am häufigsten geschwänzt hat!**
Das müsst ihr schon selbst herausfinden!
Aber die Daten auf dieser Webseite werden euch natürlich unterstützen ;-)

Wer es herausgefunden hat kann uns gern [eine Mail schreiben!](https://wahlbilanz.de/about/)


