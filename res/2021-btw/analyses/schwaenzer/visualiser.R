library("rjson")

data <- fromJSON(file="data.json")


# parties <- c ("AfD", "CDU/CSU", "Grüne", "Linke", "FDP", "SPD", "Fraktionslos");
parties <- c ("AfD", "CDU/CSU", "Grüne", "Linke", "FDP", "SPD");
partycol <- c("#009fe1","#000000","#19a329","#e0001a","#ffee00","#ff481f","#999999")


m <- matrix (nrow=6, ncol=3)
rownames(m) <- parties

m[1,] = unlist(data$AfD)
m[2,] = unlist(data$`cdu/csu`)
m[3,] = unlist(data$`Bündnis 90/Die Grünen`)
m[4,] = unlist(data$`Die Linke`)
m[5,] = unlist(data$FDP)
m[6,] = unlist(data$spd)
# m[7,] = unlist(data$fraktionslos)

#
# linke <- data$die.linke
# spd <- data$spd
# gruen <- data$gruenen
# cducsu <- data$`cdu/csu`
#
#
# schwaenzer_absolut <- c(linke$absolut, spd$absolut, gruen$absolut, cducsu$absolut)
#
#
#



pdf ("schwaenzer-bars-absolut.pdf", width=8, height=6)
barplot (m[,1], col=partycol)
dev.off ()

png ("schwaenzer-bars-absolut.png", width=800, height=600)
barplot (m[,1], col=partycol)
dev.off ()


pdf ("schwaenzer-bars-relativ.pdf", width=8, height=6)
barplot (m[,2], col=partycol)
dev.off ()

png ("schwaenzer-bars-relativ.png", width=800, height=600)
barplot (m[,2], col=partycol)
dev.off ()

