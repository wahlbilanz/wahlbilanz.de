library(gplots)
library(RColorBrewer)

# read the data
votes <- read.table (file="../../wrangling/summary-from-individuals.table", header=TRUE, sep="\t")

# coloumn 1 is just the id
m=as.matrix (votes[,2:16])
# but we can use the ids as rownames :)
rownames(m)<-votes[,1]



m[m==-1]=NA

# cluster and plot the data using gplot's heatmap.2 tool
pdf ("abstimmungscluster-from-individuals.pdf", height=20)
colfunc <- colorRampPalette(c("#FF0000FF", "#FFFF00FF"))
heatmap.2 (m, tracecol=1, cexCol=.9, margins=c(7,13),
           na.rm=TRUE, col=colfunc(15), na.color="#DDDDDDFF")
dev.off ()

png ("abstimmungscluster-from-individuals.png", height=1100)
heatmap.2 (m, tracecol=1, cexCol=.9, key=F, margins=c(7,13),
           na.rm=TRUE, col=colfunc(15), na.color="#DDDDDDFF")
dev.off ()
