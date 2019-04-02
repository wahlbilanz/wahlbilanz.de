# read the data
votes <- read.table (file="../../wrangling/summary.table", header=TRUE, sep="\t")

# coloumn 1 is just the id
m=as.matrix (votes[,2:11])
# but we can use the ids as rownames :)
rownames(m)<-votes[,1]


m[m==-1]=NA


RowVar <- function(x, ...) {
  rowSums((x - rowMeans(x, na.rm=T,  ...))^2, na.rm=T, ...)/(dim(x)[2] - 1)
}

sortedVar = sort(RowVar (m))


write.table (sortedVar, "variance.table", col.names=F)



