library(gplots)
library(RColorBrewer)
library(lattice)

# read the data
votes <- read.table (file="../../wrangling/summary-from-individuals.table", header=TRUE, sep="\t")

# coloumn 1 is just the id
m=as.matrix (votes[,2:16])
# but we can use the ids as rownames :)
rownames(m)<-votes[,1]



m[m==-1]=NA


myPanel <- function(x, y, z, ...) {
     panel.levelplot(x,y,z,...)
     panel.text(x, y, round(z,2))
}

a=dist (t(m),diag=T)


pdf ("partydist-from-individuals.pdf", height=12,width=12)
levelplot(data.matrix(a), panel = myPanel,col.regions = heat.colors(20),scales=list(x=list(rot=90)),ylab="",xlab="")
dev.off ()

png ("partydist-from-individuals.png", height=800,width=800)
levelplot(data.matrix(a), panel = myPanel,col.regions = heat.colors(20),scales=list(x=list(rot=90)),ylab="",xlab="")
dev.off ()
