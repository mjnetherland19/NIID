#!/bin/bash

path=$1
dist=$2
line=$3
refe=$4

#Determine taxon with furthest distance from all other taxa
root=$(${path}/determineRoot.py ${dist})

#Make rooted tree
Rscript ${path}/rootTree.R parsnp_out/parsnp.tree $root $line ${refe}.ref > /dev/null 2>&1
sed -i "s/.fasta//g" parsnp_out/rooted.tree
sed -i "s/.fasta//g" parsnp_out/parsnp.vcf

#Parse newick and get the order of names for SNP matrix
${path}/getNewickTreeNames.py parsnp_out/rooted.tree parsnp_out/parsnp_names

