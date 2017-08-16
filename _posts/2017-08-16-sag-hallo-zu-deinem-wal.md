---
title: "Sag »Hallo« zu deinem Wal!"
layout: post
published: true
date: 2017-08-16 20:02:24 +0200
categories:
  - Analyse
tags:
  - deinwal
  - Analyse
authors:
  - binfalse
---


{% include image.html align='alignright' url='https://deinwal.de' img='/img/wal.jpg' title='Dein Wal' caption='Du hast den Wal auf [DeinWal.de](https://deinwal.de)' %}

"Hallo Wal!" -- oder so ähnlich..
Denn [dein Wal](https://deinwal.de) ist seit gestern online! :)

Dein Wal ist dir bestimmt schonmal über den Weg gelaufen, also was soll das eigentlich?



## Das "Problem"

Wen soll ich wählen?
Diese Fragen stellen sich viele Leute, vor jeder Wahl.
Wie kann ich herausfinden, welche Partei in meinem Sinne agiert?

Wir haben im Vorfeld viele Leute gefragt: **"Wie entscheidest du, welche Partei du im September wählen wirst?".**
Die Antworten waren typischer Weise "Wahlprogramme", "Wahl-O-Mat" oder "Medien".

In Wahlprogrammen formulieren die Parteien ihre Ziele für die anstehende Legislaturperiode.
Diese Programme sind jedoch lang und schwer zu vergleichen.
Eine weitere nützliche Ressource ist der [Wahl-O-Mat](http://www.bpb.de/politik/wahlen/wahl-o-mat/), der vielen Wählern bei der Entscheidungsfindung hilft.
Allerdings basiert der Wahl-O-Mat auch auf Angaben der Parteien, denen du glauben musst.


Diese Kanäle beruhen im Wesentlichen auf Behauptungen und Versprechen -- sowohl von Kritikern, als auch von den Parteien.
Auch wenn die Aussagen auf Plausibilität geprüft werden, kann man ihnen höchstens glauben.
**Ob die Parteien ihre Versprechungen dann umsetzen bleibt ungewiss.**




## Die Lösung

Statt offene Behauptungen zu diskutieren können wir uns an die Fakten halten!

Die tatsächlichen Einstellungen der Parteien im Bundestag sind in der Regel gut dokumentiert (z.B. [bundestag.de/abstimmung](https://bundestag.de/abstimmung)).
Es bleibt aber eine Herausforderung, die Beschlüsse der verschiedenen Parteien zu sichten und mit der eigenen Einstellung zu vergleichen.
Das ist insbesondere auch schwierig, da viele Abstimmungen mit "Antrag Die Linke" oder "Antrag Bündnis 90/Die Grünen" betitelt sind, und die Ergebnisse der Parteien beeinflussend daneben stehen.

Auf [DeinWal.de](https://deinwal.de) haben wir eine Plattform entwickelt, auf der du **in einem Web-Quiz vergangene Abstimmungen nachspielen** kannst.
In einer Auswertungen werden deine Entscheidungen dann den Entscheidungen der Parteien gegenübergestellt.
Wir benutzen dabei die realen Abstimmungen der letzten Legislaturperiode und die offiziellen Abstimmungsergebnisse der  Parteien.

Dein Wal ergänzt damit eine Reihe existierender Portale, wie [abgeordnetenwatch.de](https://www.abgeordnetenwatch.de/) und den [Wahl-O-Mat](http://www.bpb.de/politik/wahlen/wahl-o-mat/).  
Wir können uns gut vorstellen, dass DeinWal.de nicht nur Erstwählern hilft, sondern  auch denjenigen, die ihre **letzte Wahlentscheidung evaluieren** wollen oder ihre Parteiverbundenheit in Frage stellen/validieren wollen.




## Umsetzung


Auf der [wahlbilanz.de]() Webseite haben wir alle Abstimmungen der letzten Legislaturperiode zusammengetragen, analysiert, und kategorisiert (mehr dazu bei [*Und Los!*](https://wahlbilanz.de/2017/06/und-los/)).
In vielen Meetings und Diskussionen wurden relevante und "machbare" Abstimmungen ausgewählt und die seitenlangen Drucksachen in möglichst einfache, verständliche Fragen übersetzt.
Manche Abstimmungen waren leider einfach zu komplex und haben es nicht in deinen Wal geschafft.
**Aus über 200 real stattgefundenen Abstimmungen haben wir 42 Fragen ausgewählt und in 12 Themengebiete unterteilt:** Familie, Arbeit, Gesundheit und Verbraucherschutz, Gesellschaft, Gentechnik in der Landwirtschaft, Bildung, Bundeswehr, Freihandelsabkommen, Energie I, Energie II, Finanzen und Inneres.



**Bei der Entwicklung haben wir hohe Priorität auf Datensouveränität gelegt.**
Quiz und Auswertungen finden komplett im Browser statt.
Im Gegensatz zu den vielen anderen Webseiten werden deine Entscheidungen nicht über das Internet verschickt oder irgendwo in einer Cloud gespeichert.
Sobald du die Webseite einmal geladen hast kannst du dein Internet gern aus machen -- dein Wal braucht es dann jedenfalls nicht mehr ;-)



Die Webseite ist mit [Angular2](https://angular.io/) entwickelt.
Angular ist ein Typescript-Framework mit dem sich clientseitige Web-Applikationen sowohl für den Desktop als auch für mobile Geräte entwickeln lassen.
Das Layout haben wir mit dem [W3.CSS Framework](https://www.w3schools.com/w3css/default.asp) gestaltet.
Das Webprojekt kompiliert zu statischem Javascript-HTML-CSS-Brei, den wir dann einfach mit einem [nginx Webserver](https://nginx.org/) mittels [Docker Container](https://www.docker.com/) ausliefern.

**Die Webseite ist übrigens Open Source:** Auf [github.com/wahlbilanz/DeinWal.de](https://github.com/wahlbilanz/DeinWal.de) könnt ihr die Webseite angucken, forken, Verbesserungsvorschläge einreichen und mitmachen!






## Einschränkungen

Zu schön um war zu sein -- wären da nicht einige Einschränkungen.

Dein Wal funktioniert ausschließlich für Parteien die in der letzten Legislaturperiode in den Bundestag gewählt wurden.
Zu Parteien wie der FDP, AFD, Piratenpartei oder Die PARTEI haben wir leider keine Abstimmungsergebnisse.

Des weiteren gibt es zwischen CDU/CSU und SPD eine Koalitionsvertrag, an den sich beide Fraktionen halten wollen/müssen.
Wenn SPD für X stimmt, muss das also nicht heißen, dass sie X bevorzugen.
Vielleicht hatte X bei den Verhandlungen nur geringere Priorität als Y, und es war ihnen wichtiger, dass CDU/CSU für Y stimmen (siehe [Über Fraktionsdisziplin und den Koalitionsvertrag](https://wahlbilanz.de/2017/06/ueber-fraktionsdisziplin-und-den-koalitionsvertrag/)).
Und umgekehrt natürlich..
Nichtsdestotrotz haben die Parteien aber so abgestimmt wie sie haben! ;-)

Bei den Oppositionsparteien kann man sich im Gegenzug auch nicht sicher sein ob sie bei einer Abstimmung aus Überzeugung gestimmt haben oder nur der herrschenden Politik Widerstand und Ablehnung entgegenbringen wollten.
Aber auch hier gilt: Abgestimmt ist abgestimmt.

Es heisst nicht umsonst Politik.





## Hilf mit!

Auch wenn die Webseite schonmal ganz gut funktioniert können wir deine Hilfe immer gut gebrauchen.
Egal ob du einen Bug gefunden hast oder uns nur sagst wie lange du für das Quiz gebraucht hast und ob was (un)erwartetes herausgekommen ist -- **dein Feedback ist sehr Willkommen! :)**  
Erstelle ein [Ticket auf GitHub](https://github.com/wahlbilanz/DeinWal.de/issues/new) oder [schick uns eine Mail](https://deinwal.de/impressum).



