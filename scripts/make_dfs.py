import pandas as pd
import glob 
import re
import os
import warnings
warnings.filterwarnings("ignore")

def make_checkm():

    with open("checkm_out/checkm.out","r") as check, open("dataframes/checkm.csv","w") as writ:
        for c in check:
            if re.search("INFO",c) or re.search("-",c):
                continue
            else:
                line=c.strip().split()
                if re.search("Completeness",c):
                    header=[line[0]]+line[-4:-2]
                    header.append(f"{line[-2]} {line[-1]}")
                else:
                    values=[line[0]]+line[-3:]
        writ.write(",".join(header) + "\n")
        writ.write(",".join(values) + "\n")

def make_mlst():
    header=["Scheme","ST-type"]
    values=[]

    with open("mlst.out","r") as mlst:
        for m in mlst:
            line=m.strip().split()

    values.append(line[1])
    values.append(line[2])

    line=line[3:]

    for l in line:
        allele=l.split("(")
        header.append(allele[0])
        values.append(allele[1][:-1])
    
    with open("dataframes/mlst.csv","w") as writ:

        writ.write(",".join(header) + "\n")
        writ.write(",".join(values) + "\n")

def make_profile():
    df=pd.read_csv("genomes_mash.csv",index_col=0)
    df=df[["Query","Distance","P-value"]]

    df["Distance"]=df["Distance"].apply(lambda x: round(x,4))
    df["P-value"]=df["P-value"].apply(lambda x: "<0.001" if x < 0.001 else x)

    df.to_csv("dataframes/profile.csv",index=False)

def make_quast():
    header=""
    values=""
    with open("quast_out/report.txt","r") as quast, open("dataframes/stats.csv","w") as writ:
        for q in quast:
            line=q.strip().split()
            if re.search("Assembly",q) or len(line) > 5:
                continue
            elif len(line) > 0:
                label=line[:-1]
                label=" ".join(label)
                header+=f"{label},"
                values+=f"{line[-1]},"
                if re.search("N50",q):
                    break

        writ.write(header[:-1] + "\n")
        writ.write(values[:-1] + "\n")

def make_plasmid():
    header=["SEQUENCE","START","END","%COVERAGE","%IDENTITY","DATABASE"]

    df=pd.read_csv("plasmid.out",index_col=0,sep="\t")

    df3=df[header]

    df3.to_csv("dataframes/plasmid.csv",index=False)

def make_vf():
    header=["SEQUENCE","START","END","STRAND","GENE","%COVERAGE","%IDENTITY","DATABASE","PRODUCT"]

    df=pd.read_csv("vfdb_results.tsv",index_col=0,sep="\t")

    df3=df[header]

    df3["PRODUCT"]=df3["PRODUCT"].apply(lambda x: " ".join(x.split(")")[1].split()[:5]))
    df3["PRODUCT"]=df3["PRODUCT"].apply(lambda x: x.split("(")[0])
    df3["PRODUCT"]=df3["PRODUCT"].apply(lambda x: x.split("[")[0])

    df3.to_csv("dataframes/vf_df.csv",index=False)

def make_amr():

    header=["SEQUENCE","START","END","STRAND","GENE","%COVERAGE","%IDENTITY","DATABASE","RESISTANCE"]

    globs=glob.glob("*amr*tsv")

    if len(globs) == 0:
        return

    df=pd.read_csv(globs[0],index_col=0,sep="\t")
    df1=pd.read_csv(globs[1],index_col=0,sep="\t")
    df2=pd.read_csv(globs[2],index_col=0,sep="\t")

    df3=pd.concat([df,df1,df2])

    df3=df3[header]

    df3=df3.replace("card","CARD")
    df3=df3.replace("ncbi","AMRFinderPlus")
    df3=df3.replace("argannot","ARG-ANNOT")

    df3.to_csv("dataframes/amr_df.csv",index=False)

def make_core_gene():

    seq={}

    with open("parsnp_out/log/parsnpAligner.log","r") as core, open("dataframes/core_gene.csv","w") as writ:
        writ.write("Genome,Core Gene Fraction\n")
        for c in core:
            if re.search("Sequence",c):
                if re.search("fasta.ref",c):
                    continue
                else:
                    line=c.strip().split()
                    genome=line[-1].split("/")[-1].split(".")[0]
                    seq[line[1]]=genome
            elif re.search("sequence ",c):
                line=c.strip().split()
                num=line[-2][0]
                perc=line[-1]
                if num in seq.keys():
                    writ.write(f"{seq[num]},{perc}\n")

if os.path.exists("quast_out/report.txt"):
        make_quast()
if os.path.exists("checkm_out/checkm.out"):
        make_checkm()
if os.path.exists("genomes_mash.csv"):
        make_profile()
if os.path.exists("mlst.out"):
        make_mlst()
if os.path.exists("vfdb_results.tsv"):
        make_vf()
if os.path.exists("plasmid.out"):
        make_plasmid()
if os.path.exists("parsnp_out/log/parsnpAligner.log"):
        make_core_gene()

make_amr()
