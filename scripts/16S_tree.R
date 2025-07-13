suppressPackageStartupMessages(library(ape))
args = commandArgs(trailingOnly=TRUE)

tree=ape::read.tree(file=args[1])
tr=root(tree,args[2], resolve.root=T)

line=args[4]
tree=ape::read.tree(file=args[1])
df=as.data.frame(cophenetic(tree))
df=df[order(df[[line]]),]
df = subset(df, select = c(args[2]))
hold<-rownames(df)[2]
write(hold,"target")

tr=ladderize(tr, right = TRUE)

png(file=paste0(args[3],"_16S_tree.png"),width=1000, height=1000)
plot.phylo(tr, cex=2.3,use.edge.length=F,edge.width=3)
dev.off()

write.tree(tr,paste0(args[3],"_rooted.nwk")
