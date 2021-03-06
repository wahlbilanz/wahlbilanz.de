library(gplots)
library(RColorBrewer)

# read the data
votes <- read.table (file="../../wrangling/summary.table", header=TRUE, sep="\t")

# coloumn 1 is just the id
m=as.matrix (votes[,2:11])
# but we can use the ids as rownames :)
rownames(m)<-votes[,1]



m[m==-1]=NA

# cluster and plot the data using gplot's heatmap.2 tool
pdf ("abstimmungscluster.pdf", height=20)
colfunc <- colorRampPalette(c("#FF0000FF", "#FFFF00FF"))
heatmap.2 (m, tracecol=1, cexCol=.9, margins=c(12,17),
           na.rm=TRUE, col=colfunc(15), na.color="#DDDDDDFF")
dev.off ()
