library(gplots)
library(RColorBrewer)

# read the data
votes <- read.csv ("Lokalomat.csv", header=T)

# coloumn 1 is just the id
# we're interested in coloumns 2-10
m=as.matrix (votes[,2:10])
# but we can use the ids as rownames :)
rownames(m)<-votes[,1]



# cluster and plot the data using
# gplot's heatmap.2 tool
pdf ("abstimmungscluster.pdf", height=20)
colfunc<-colorRampPalette(c("#FF0000FF","#FFFF00FF"))
heatmap.2 (m, tracecol=1, cexCol=.9, margins=c(6,14),
   na.rm=TRUE, col=colfunc(15), na.color="#DDDDDDFF")
dev.off ()

