suppressPackageStartupMessages(library(ape))
args = commandArgs(trailingOnly=TRUE)

tree=ape::read.tree(file=args[1])
tree <- drop.tip(tree, args[4])
tr=root(tree,args[2], resolve.root=T)
tr=ladderize(tr, right = TRUE)

png(file=paste0("parsnp_out/",args[3],"_parsnp_tree.png"),width=1000, height=1000)
plot.phylo(tr, cex=2.3,use.edge.length=F,edge.width=3)
dev.off()

write.tree(tr,"parsnp_out/rooted.tree")
