#!/bin/env python3
import sys

#Takes mash .tsv file as input

d={}
num=0
with open(sys.argv[1],"r") as mash:
    F=[x.strip() for x in mash]

for value in F:
    line=value.split('\t')
    ref=line[0]
    dist=line[2]
    Ref=ref.split('/')[-1]
    if Ref not in d.keys():
        d[Ref]=[float(dist)]
    else:
        d[Ref].append(float(dist))

for key in d.keys():
    amt=sum(d[key])/len(d[key])
    #print(f"{key}: {d[key]}, {amt}")
    if amt > num:
        name=key
        num=amt
print(name)
