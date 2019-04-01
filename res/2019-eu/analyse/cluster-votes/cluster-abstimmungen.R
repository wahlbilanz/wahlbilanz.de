library(gplots)
library(RColorBrewer)

# read the data
votes <- read.table (file="../../wrangling/summary.table", header=TRUE, sep="\t")

# coloumn 1 is just the id
m=as.matrix (votes[,2:11])
# but we can use the ids as rownames :)
rownames(m)<-votes[,1]


# rename the coloumns -> proper party names
# colnames(m)<-sapply (colnames(m), function (x) {
# 	if (startsWith (x, "grue"))
# 	{
# 		"Bündnis 90/Die Grünen"
# 	}
# 	else if (startsWith (x, "cdu"))
# 	{
# 		"CDU/CSU"
# 	}
# 	else if (startsWith (x, "die"))
# 	{
# 		"DIE LINKE"
# 	}
# 	else if (startsWith (x, "frak"))
# 	{
# 		"Fraktionslos"
# 	}
# 	else if (startsWith (x, "spd"))
# 	{
# 		"SPD"
# 	}
# 	else
# 	{
# 		x
# 	}
# })

m[m==-1]=NA

# cluster and plot the data using gplot's heatmap.2 tool
pdf ("abstimmungscluster.pdf", height=20)
colfunc <- colorRampPalette(c("#FF0000FF", "#FFFF00FF"))
heatmap.2 (m, tracecol=1, cexCol=.9, margins=c(12,17),
           na.rm=TRUE, col=colfunc(15), na.color="#DDDDDDFF")
dev.off ()


RowVar <- function(x, ...) {
  rowSums((x - rowMeans(x, na.rm=T,  ...))^2, na.rm=T, ...)/(dim(x)[2] - 1)
}
