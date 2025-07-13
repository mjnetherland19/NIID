#!/bin/env python3

from fpdf import FPDF
#from fpdf.fonts import FontFace
import csv
import pandas as pd
import re
from PIL import Image
import os
import glob as glob
import sys

class PDF(FPDF):
    def header(self):
        self.set_font("helvetica", "B", 12)
        # Moving cursor to the right:
        self.cell(80)
        # Printing title:
        self.cell(30, 10, f"Isolate Analysis - {path}", align="C")
        # Performing a line break:
        self.ln(10)

    def footer(self):
        # Position cursor at 1.5 cm from bottom:
        self.set_y(-15)
        self.set_font("helvetica", "I", 8)
        # Printing page number:
        self.cell(0, 10, f"Page {self.page_no()}/{{nb}}", align="C")
                
def section(title,tool):
    pdf.ln(10)
    pdf.set_font("Times", size=18)
    pdf.cell(40, 10, f"{title}")
    pdf.ln(10)
    pdf.set_font("Times", size=12)
    pdf.cell(60, 10, f"Tool Used: {tool}")
    pdf.ln(10)
    pdf.set_font("helvetica", "B", 8)

def snp_image(path):
    im = Image.new(mode = "RGB", size = (2100, 1900), color = (255, 255, 255))

    img2 = Image.open(glob.glob(f"{path}/parsnp_out/*_parsnp_tree.png")[0])
    img3 = Image.open(glob.glob(f"{path}/parsnp_out/*_snps_matrix.png")[0])
    width,height=img2.size
    #left, top, right, bottom
    cr2=img2.crop((85,0,width,height))
    
    re_im2 = cr2.resize((round(cr2.size[0]*1.10), round(cr2.size[1]*1.10)))
    re_im3 = img3.resize((round(img3.size[0]*0.25), round(img3.size[1]*0.25)))

    #im.paste(img2, (0,30))
    im.paste(re_im2, (0,20))
    im.paste(re_im3, (950,25))

    return im

def no_res(line):

    with pdf.table(cell_fill_color=greyscale, cell_fill_mode="ROWS",text_align="CENTER") as table:
        row=table.row()
        row.cell(f"No {line} results")

def assemble():
    #Assembly Stats

    section(f"Assembly Statistics","MEGAHIT")
    with pdf.table(cell_fill_color=greyscale, cell_fill_mode="ROWS",text_align=("CENTER")) as table:
        for data_row in assem:
            row = table.row()
            for datum in data_row:
                if len(datum) > 3:
                    if datum.isdigit():
                        row.cell(f"{int(datum):,}")
                    else:
                        row.cell(datum)
                else:
                    row.cell(datum)

def checkm():
    #CheckM
    section("CheckM Statistics","CheckM")
    with pdf.table(text_align=("CENTER"),cell_fill_color=greyscale, cell_fill_mode="ROWS") as table:
        for data_row in check:
            row = table.row()
            for datum in data_row:
                row.cell(datum)

def profile():
    #Profile
    section("Taxonomic Identification","Mash")
    with pdf.table(text_align=("CENTER"),cell_fill_color=greyscale, cell_fill_mode="ROWS") as table:
        for data_row in profile:
            row = table.row()
            for datum in data_row:
                row.cell(datum)

def mlst():
    #MLST
    section("MLST Sequence Typing","PubMLST")
    widths=[30]
    top=mlst[0]
    for t in top:
        widths.append(15)

    if len(mlst)==1:
        no_res("MLST")
    else:
        with pdf.table(cell_fill_color=greyscale, cell_fill_mode="ROWS",text_align=("CENTER"),col_widths=widths) as table:
            for data_row in mlst:
                row = table.row()
                for datum in data_row:
                    row.cell(datum)
    #pdf.ln(15)
    #pdf.image(f"{docs}/novel_mlst.png", h=13, w=28)
    #pdf.image(f"{docs}/mlst_explanation.png", h=33, w=76, x=pdf.epw/2,y=pdf.eph*0.7) 

def plasmid():   
    #Plasmid
    section("Plasmid Results","ABRicate")
    if len(plasmid)==1:
        no_res("plasmid")
    else:
        with pdf.table(cell_fill_color=greyscale, cell_fill_mode="ROWS",text_align="CENTER") as table:
            for data_row in plasmid:
                row = table.row()
                for datum in data_row:
                    row.cell(datum)
def amr():            
    #AMR
    section("AMR Results","ABRicate")
    if len(amr)==1:
        no_res("AMR")
    else:
        with pdf.table(cell_fill_color=greyscale, cell_fill_mode="ROWS",text_align="CENTER", col_widths=(28,17,15,20,30,30,25,35,40)) as table:
            for data_row in amr:
                row = table.row()
                for datum in data_row:
                    row.cell(datum)
def vf():            
    #VF
    section("VF Results","ABRicate")
    if len(vf)==1:
        no_res("VF")
    else:
        with pdf.table(cell_fill_color=greyscale, cell_fill_mode="ROWS",text_align="CENTER", col_widths=(28,17,15,20,30,30,25,35,40)) as table:
            for data_row in vf:
                row = table.row()
                for datum in data_row:
                    row.cell(datum)

def phylogeny():
    #16S
    pdf.add_page()

    pdf.set_font("Times", size=18)
    pdf.cell(40, 10, "16S Phylogeny")
    pdf.ln(10)
    pdf.set_font("Times", size=12)
    pdf.cell(60, 10, f"Tool Used: MAFFT - FastTree")
    pdf.ln(10)
    pdf.set_font("helvetica", "B", 8)
    pdf.image(f"{glob.glob(f'{path}/genomes_16S_tree.png')[0]}", h=150, w=150,x=50)

def snp():
    #SNP Analysis
    pdf.add_page()
    pdf.set_font("Times", size=18)
    pdf.cell(40, 10, "SNP Analysis")
    pdf.ln(10)
    pdf.set_font("Times", size=12)
    pdf.cell(60, 10, f"Tool Used: Parsnp")
    pdf.ln(10)
    pdf.set_font("helvetica", "B", 8)
    pdf.image(snp_image(path),h=190,w=210)

    with pdf.table(cell_fill_color=greyscale, cell_fill_mode="ROWS",text_align="CENTER", col_widths=(30,20)) as table:
        for data_row in core:
            row = table.row()
            for datum in data_row:
                row.cell(datum)

path=sys.argv[1]
base=f"{path}/dataframes"

pdf = PDF()
pdf.add_page()

ezlight_blue = (0, 176, 240)
greyscale = (231, 230, 230)
#headings_style = FontFace(fill_color=ezlight_blue,color=(255,255,255))

if os.path.exists(f"{base}/stats.csv"):
    with open(f"{base}/stats.csv") as csv_file:
        assem = list(csv.reader(csv_file, delimiter=","))
        assemble()
if os.path.exists(f"{base}/checkm.csv"):
    with open(f"{base}/checkm.csv") as csv_file:
        check = list(csv.reader(csv_file, delimiter=","))
        checkm()
if os.path.exists(f"{base}/profile.csv"):
    with open(f"{base}/profile.csv") as csv_file:
        profile = list(csv.reader(csv_file, delimiter=","))
        profile()
if os.path.exists(f"{base}/mlst.csv"):
    with open(f"{base}/mlst.csv") as csv_file:
        mlst = list(csv.reader(csv_file, delimiter=","))
        mlst()
if os.path.exists(f"{base}/plasmid.csv"):
    with open(f"{base}/plasmid.csv") as csv_file:
        plasmid = list(csv.reader(csv_file, delimiter=","))
        plasmid()
if os.path.exists(f"{base}/amr_df.csv"):
    with open(f"{base}/amr_df.csv") as csv_file:
        amr = list(csv.reader(csv_file, delimiter=","))
        amr()
if os.path.exists(f"{base}/vf_df.csv"):
    with open(f"{base}/vf_df.csv") as csv_file:
        vf = list(csv.reader(csv_file, delimiter=","))
        vf()
if os.path.exists(f"{path}/genomes_16S_tree.png"):
    phylogeny()
if os.path.exists(f"{base}/core_gene.csv"):
    with open(f"{base}/core_gene.csv") as csv_file:
        core = list(csv.reader(csv_file, delimiter=","))
        snp()

pdf.output(f"{path}/{path}_isolate_report.pdf")
