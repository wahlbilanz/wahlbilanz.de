d=read.table("distances.txt")
sapply(1:9, function (i) sapply (i:9,function (j) d[i,j]<<-d[j,i]))



coords<-function (theta) {
print (1000*sin(theta)-301)
print (1000*sin(theta)+301)
print (1000*cos(theta)-301)
print (1000*cos(theta)+301)
}
