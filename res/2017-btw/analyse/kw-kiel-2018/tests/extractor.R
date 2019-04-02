library(gplots)
library(RColorBrewer)

prefs=read.csv ("Lokalomat.csv", header=T)
m=as.matrix (prefs[2:10])
row.names(m)<-prefs[,1]


colfunc <- colorRampPalette(c("#FF0000FF", "#FFFF00FF"))

# heatmap.2 (m, tracecol=1, cexCol=.9, margins=c(6,15),na.rm=TRUE, col=colfunc(15), na.color="#DDDDDDFF")


d=matrix (0, 9,9)
rownames(d)<-colnames(m)
colnames(d)<-colnames(m)

sapply (1:8, function (i) sapply ((i+1):9, function (j) {
        d[i,j]<<-sum(m[,i]*m[,j])
        d[j,i]<<-sum(m[,i]==m[,j])
}))


png ("heatmap-distance.png", width=800, height=800)
image(d)
dev.off ()

library(reshape2)
library(ggplot2)

frequencies_df = melt(d)
names(frequencies_df) = c('party1', 'party2', 'similarity')

png ("bubbleplot.png", width=800, height=800)
ggplot(frequencies_df, aes(x = party1, y = party2, size = similarity)) + geom_point()
dev.off ()


png ("bubbleplot-log.png", width=800, height=800)
ggplot(frequencies_df, aes(x = party1, y = party2, size = log((similarity-5)*10))) + geom_point()
dev.off ()





png ("bubbleplot-log-scale.png", width=800, height=800)
ggplot(frequencies_df, aes(x = party1, y = party2, size = log((similarity)/29))) + geom_point()
dev.off ()




f=matrix (0, 9,9)
rownames(f)<-colnames(m)
colnames(f)<-colnames(m)

sapply (1:8, function (i) sapply ((i+1):9, function (j) {
        f[i,j]<<-sum(m[,i]*m[,j])
        f[j,i]<<-sum(m[,i]*m[,j])
        #       d[j,i]<<-sum(m[,i]==m[,j])
}))

png ("heatmap-distance-a.png", width=800, height=800)
image(f)
dev.off ()



g=matrix (0, 9,9)
rownames(g)<-colnames(m)
colnames(g)<-colnames(m)

sapply (1:8, function (i) sapply ((i+1):9, function (j) {
        g[j,i]<<-sum(m[,i]==m[,j])
        g[i,j]<<-sum(m[,i]==m[,j])
}))

png ("heatmap-distance-b.png", width=800, height=800)
image(g)
dev.off ()





g=matrix (0, 9,9)
rownames(g)<-colnames(m)
colnames(g)<-colnames(m)

sapply (1:8, function (i) sapply ((i+1):9, function (j) {
        g[j,i]<<-sum(m[,i]==m[,j])
        g[i,j]<<-sum(m[,i]==m[,j])
}))

png ("heatmap-distance-b-log.png", width=800, height=800)
image(log(g))
dev.off ()





h=matrix (0, 9,9)
rownames(h)<-colnames(m)
colnames(h)<-colnames(m)

sapply (1:8, function (i) sapply ((i+1):9, function (j) {
#       h[j,i]<<-sum(m[,i]*m[,j])
        h[i,j]<<-sum(m[,i]==m[,j])
}))


frequencies_h = melt(h)
names(frequencies_h) = c('party1', 'party2', 'similarity')

png ("bubbleplot-a.png", width=800, height=800)
ggplot(frequencies_h, aes(x = party1, y = party2, size = log(similarity))) + geom_point()
dev.off ()
