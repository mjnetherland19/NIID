#!/bin/bash

grab()
{
	${SCRIPT_DIR}/scripts/filter_records.py $1
	${SCRIPT_DIR}/scripts/best_genome.py genome_records.tsv $2
	sed -i '1d' temp_best
	cat temp_best | cut -d, -f4-5 > curated_accessions

}	

download_genomes()
{
	while read line
	do
		strain=$(echo $line | cut -d, -f1)
		ftp=$(echo $line | cut -d, -f2)
		genome_name=$(echo $ftp | rev | cut -d/ -f1 | rev) #GCA_024668725.3_ASM2466872v3
		
		#Replace ftp with https, put into var
		var="${ftp/ftp/https}"
		
		#Get the record file
		rec=$(wget -qO- $var)
		assembly_link=$(echo $rec | grep -Po "(?<=>)${genome_name}_genomic.fna.gz")
		
		wget ${var}/${assembly_link} #to filename = ${assembly_link::-3}
		gunzip $assembly_link
		
		assembly_link=${assembly_link::-3}
		
		if [ $num -eq 1 ]
		then
			mv ${assembly_link} "${out}/${1// /_}.fasta"
		else
			mv ${assembly_link} "${out}/${1// /_}_${strain// /_}.fasta"
		fi
		
	done<curated_accessions
}

query_ncbi()
{
	
	name=$1
	ref=$2
	esearch -db assembly -query "${name}" < /dev/null | efetch -format docsum | xtract -pattern DocumentSummary -def "N/A" -element SpeciesTaxid -element SpeciesName -element Sub_value -element FtpPath_GenBank -element assembly-status -element FromType -element RefSeq_category -division Meta -block Stats -element Stat > temp.tsv
}

list=$1
out=$2
num=$3
SCRIPT_DIR=$4


if [ ! -d $out ]
then
	mkdir $out
fi

while read line
do
	query_ncbi "${line}"
	
	grep "from type" temp.tsv > type_strains
	num1=$(wc -l type_strains | cut -d" " -f1)
	if [ $num1 -eq 0 ]
	then
		grep "represent" temp.tsv > ref_strains
		num2=$(wc -l ref_strains | cut -d" " -f1)
		if [ $num2 -eq 0 ]
		then
			grep "Complete Genome" temp.tsv > complete_strains
			num3=$(wc -l complete_strains | cut -d" " -f1)
			if [ $num3 -eq 0 ]
			then
				grep "Chromosome" temp.tsv > chrom_strains
				num4=$(wc -l chrom_strains | cut -d" " -f1)
				if [ $num4 -eq 0 ]
				then
					grep "Scaffold" temp.tsv > scaff_strains
					num5=$(wc -l scaff_strains | cut -d" " -f1)
					if [ $num5 -eq 0 ]
					then
						grep "Contig" temp.tsv > contig_strains
						num6=$(wc -l contig_strains | cut -d" " -f1)
						if [ $num6 -eq 0 ]
						then
							echo $line
						else
							grab contig_strains $num
						fi
					else
						grab scaff_strains $num
					fi
				else
					grab chrom_strains $num
				fi
			else
				grab complete_strains $num
			fi
		else
			grab ref_strains $num
		fi
	else
		grab type_strains $num
	fi
	
	download_genomes "${line}"
	
done<${list}

rm *_strains
rm temp*
rm curated_accessions
