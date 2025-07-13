## NCBI Isolate ID (NIID pipeline)
Pronounced NEED. This is a database-independent pipeline for bacterial genome assembly, identification, annotation, phylogenetics, etc. At the end of the pipeline the results are packaged into a PDF report, for easy viewing and sharing. The pipeline can only be used with paired reads.

'NCBI is a part of the pipeline name because primary taxonomic identification is conducted using a MinHash table of a recent set of 21,258 genomes published by [NCBI](https://ncbiinsights.ncbi.nlm.nih.gov/2025/01/14/updated-bacterial-and-archaeal-reference-genome-collection-2/)

## Overview
The pipeline follows this sequence (although each stage can be run independently):
| Stage        | Tool                       |
|:-------------:|:-------------------------:|
| Assembly       | MEGAHIT                  |
| Quality check  | CheckM                   |
| Assembly Stats | QUAST                    |
| Taxonomic ID   | Mash                     |
| 16S Phylogeny  | HMMER - MAFFT - FastTree |
| MLST           | [tseemann/mlst](https://github.com/tseemann/mlst/tree/master)|
| Genome profile | [ABRicate](https://github.com/tseemann/abricate) - Virulence Factor, AMR, Plasmid|
| Annotation     | Prokka |
| SNP Analysis   | Parsnp |
| Report Generatoin| fpdf2 |

## Report Example (First page only)
The full report can be found in the repo.
<img width="763" height="727" alt="image" src="https://github.com/user-attachments/assets/24f135d5-0516-43e1-8a30-6dcdcdb80866" />



## Installation
You will need to set up three conda environments:

- conda create -n NIID -c conda-forge -c bioconda -c defaults abricate megahit checkm quast hmmer mlst mash mafft prokka seqtk entrez-direct

- conda create -n parsnp-env -c bioconda parsnp

- conda create -n fpdf2 fpdf2 pandas pillow csv

- Download the MinHash table from [Zenodo](https://zenodo.org/records/15871983)

- Finally, clone this repo

## Usage
By default, all stages of the pipeline are turned on. Run the whole workflow with:

./NIID_pipeline \<file\>

\<file\> is a list of directory names, where your sequences data is stored.

The pipeline expects the directory name to also be in the sequence file name according to this format: ${dir}\*1.fast\* ${dir}\*2.fast\*

---

Any number of stages can be run separately with this command:
./NIID_pipeline --only \<stage name\>, \<stage name\>, ... \<file\>

\<stage name\> is any keyword from this list: 'assemble' 'checkm' 'quast' 'plasmid' 'profile' 'phylogeny' 'mlst' 'parsnp' 'amr' 'vf' 'prokka'

---

Some stages can only be run if preceding stages have already occurred. The pipeline will catch any mistakes and inform you of the appropriate stage to run.

## Phylogeny
- The phylogenetic inference is conducted on a 16S multisequence alignment of the top 5 taxa given by Mash.
- Genomes of these taxa are downloaded using NCBI's Entrez Direct. Type strain genomes are always downloaded preferentially, if they are available
  - This operation may take a long time if the taxon has many assemblies in NCBI
- An HMM was constructed from the Stokholm alignment found in [NCBI's ribovore program](https://github.com/ncbi/ribovore) and it is used to extract the 16S region of the 

