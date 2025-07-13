#!/bin/bash

dir=$1
script_dir=$2
outt=$3

if [ ! -d hmmer_res ]
then
	mkdir hmmer_res
fi

for fasta in ${dir}/*
do

	name=$(basename $fasta)
	change=${name:0:-6}
	nhmmscan --dfamtblout hmmer_res/${name}.res --noali ${script_dir}/data/HMM/16S_ribovore.hmm $fasta > /dev/null

	python3 ${script_dir}/scripts/parse_hmmer_2.py hmmer_res/${name}.res RNA > coords

	sort -k3 -n -t, -r coords > sorted_coords
	echo $name
	cat sorted_coords
	echo
	while read line
	do
		seq=$(echo $line | cut -d, -f1)
		strand=$(echo $line | cut -d, -f2)
		length=$(echo $line | cut -d, -f3)
		out=${seq}

		if [ $strand == "-" ]
		then
			samtools faidx --mark-strand sign -i ${fasta} ${seq} >> ${outt}/${dir}.multifasta


		elif [ $strand == "+" ]
		then	
			samtools faidx --mark-strand sign ${fasta} ${seq} >> ${outt}/${dir}.multifasta	
		else
			echo $res >> extract.err
		fi	
		
		sed -i "s/${seq}(${strand})/$change/g" ${outt}/${dir}.multifasta

		break

	done<sorted_coords
done

#rm coords sorted_coords
