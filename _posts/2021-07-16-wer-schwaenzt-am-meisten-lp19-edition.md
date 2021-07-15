---
title: "Wer schwänzt am meisten? 2021 Edition"
layout: post
published: true
date: 2021-07-16 00:40:46 +0200
categories:
  - Hintergrund
  - Analyse
tags:
  - Disziplin
  - Analyse
  - R
  - Python
  - btw19
authors:
  - binfalse
---

Schon die persischen Könige wussten: Neue Wahl neue Daten.
Und spätestens seit der letzten Wahl wissen wir, das wir mit neuen Daten auch wieder [die Schwänzer-Statistik berechnen](/2017/07/wer-schwaenzt-am-meisten/) können!
Und weil explizit danach gefragt wurde: Hier ist die Edition für die 19. Legislaturperiode :)

(Die Berechnung hab ich analog zum letzten Mal gemacht.)





## Was sagen die Zahlen?

Also absolut gesehen hat sich, im Vergleich mit der vorherigen Legislaturperiode, nicht so viel geändert:

{% include image.html url='/res/2021-btw/analyses/schwaenzer/schwaenzer-bars-absolut.pdf' img='/res/2021-btw/analyses/schwaenzer/schwaenzer-bars-absolut.png' title='Wer schwänzt am meisten?' caption='Wer schwänzt am meisten?' %}

*CDU/CSU* sichert sich wieder die Pole-Position mit 4748 verpassten Stimmen, gefolgt von der *SPD* mit 3783 Schwänzungen.
*AfD* und *Die Linke* liegen sehr nah beieinander auf den Plätzen drei und vier.
Am besten scheinen *Die Grünen* abzuschneiden mit nur 1512 geschwänzten Stimmen.



Aber wie schon [beim letzten Mal erklärt,](/2017/07/wer-schwaenzt-am-meisten/) muss man mit Zahlen immer vorsichtig umgehen; insbesondere mit absoluten Zahlen!
Die Fraktionen haben natürlich unterschiedlich viele Mitglieder im Bundestag sitzen und damit unterschiedlich viele potentielle Stimmen.
Selbst wenn bei jeder Abstimmung die Hälfte jeder Fraktion schwänzen würde, hätten CDU/CSU an dieser Stelle "gewonnen"!
Denn 50% geschwänzte Stimmen von *CDU/CSU* sind einfach mehr als 50% der *FDP*.


Gucken wir uns also die relativen Zahlen an, also wie viele der verfügbaren Stimmen wurden geschwänzt:



{% include image.html url='/res/2021-btw/analyses/schwaenzer/schwaenzer-bars-relativ.pdf' img='/res/2021-btw/analyses/schwaenzer/schwaenzer-bars-relativ.png' title='Wer schwänzt am meisten?' caption='Wer schwänzt am meisten? Also relativ gesehen, jetzt...' %}


Und wieder ergibt sich ein gänzlich anderes Bild: *CDU/CSU* sind plötzlich die fleißigsten Abgeordneten!?

Der Schwänzer-Highscore in der 19. Legislaturperiode wird angeführt von *Die Linke* (38.03% versäumte Stimmen), gefolgt von der *AfD* (30.30% versäumte Stimmen).


## Daten und Skripte

Die Daten wurden mit einem [Python-Skript](https://github.com/wahlbilanz/wahlbilanz.de/tree/master/abstimmungen/applications/schwaenzer-19.py) erzeugt, das meinen Abstimmungsparser benutzt. Die Visualisierung hat wieder ein [R-Skript](https://github.com/wahlbilanz/wahlbilanz.de/blob/master/res/2021-btw/analyses/schwaenzer/visualiser.R) übernommen.

Die Daten sehen wie folgt aus:



| Partei | Absolut geschwänzt | Relativ geschwänzt | Anzahl teilgenommene Abstimmungen |
| ------ | ------------------:| ------------------:| ---------------------------------:|
| AfD |  2732 |  30.30 | 240 |
| Bündnis 90/Die Grünen | 1512 | 22.57 | 240 |
| Die Linke | 2624 | 38.03 | 240 |
| FDP | 1990 | 24.88 | 240 |
| CDU/CSU | 4748 | 19.31 | 240 |
| SPD | 3783 | 24.87 | 240 |


## Disclaimer

Wieder gilt: Die Relevanz der Daten ist "relativ" fragwürdig.
Einige vertreten sogar die Auffassung, dass diejenigen, die eine Bundestagssitzung schwänzen, wahrscheinlich gerade einfach an wichtigeren Dingen arbeiten.
Falls euch das Thema weiter interessiert könnt ihr die Daten auf dieser Webseite und dem zugehörigen GitHub-Projekt gern nutzen.
Und am besten kontaktiert ihr direkt die Abgeordneten, die ungewöhnlich viele Abstimmungen verpassen!?

Lasst mich gern wissen, wenn ihr etwas spannendes herausbekommt :)


