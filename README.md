## NCBI Isolate ID (NIID pipeline)
Pronounced NEED. This is a database-independent pipeline for bacterial genome assembly, identification, annotation, phylogenetics, etc. At the end of the pipeline the results are packaged into a PDF report, for easy viewing and sharing.

'NCBI is a part of the pipeline name because primary taxonomic identification is conducted using a MinHash table of a recent set of 21,258 genomes published by [NCBI](https://ncbiinsights.ncbi.nlm.nih.gov/2025/01/14/updated-bacterial-and-archaeal-reference-genome-collection-2/)

## Installation
You will need to set up three conda environments:

conda create -n NIID -c conda-forge -c bioconda -c defaults abricate megahit checkm quast hmmer mlst mash mafft prokka seqtk
conda create -n parsnp-env -c bioconda parsnp==2.* 
conda create -n fpdf2 fpdf2 pandas pillow csv

Download the MinHash table from [Zenodo](https://zenodo.org/records/15871983)

