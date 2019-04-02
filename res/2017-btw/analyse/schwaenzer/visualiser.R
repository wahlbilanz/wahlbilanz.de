library("rjson")

data <- fromJSON(file="data.json")


parties <- c ("Die Linke", "SPD", "Die Grünen", "CDU/CSU", "Fraktionslos");

m <- matrix (nrow=5, ncol=3)
rownames(m) <- parties

m[1,] = unlist(data$die.linke)
m[2,] = unlist(data$spd)
m[3,] = unlist(data$gruenen)
m[4,] = unlist(data$`cdu/csu`)
m[5,] = unlist(data$fraktionslos)

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
barplot (m[,2], col=c("#e0001a","#ff481f","#19a329","#000000","#999999"))
dev.off ()

png ("schwaenzer-bars-absolut.png", width=800, height=600)
barplot (m[,2], col=c("#e0001a","#ff481f","#19a329","#000000","#999999"))
dev.off ()


pdf ("schwaenzer-bars-relativ.pdf", width=8, height=6)
barplot (m[,1], col=c("#e0001a","#ff481f","#19a329","#000000","#999999"))
dev.off ()

png ("schwaenzer-bars-relativ.png", width=800, height=600)
barplot (m[,1], col=c("#e0001a","#ff481f","#19a329","#000000","#999999"))
dev.off ()

