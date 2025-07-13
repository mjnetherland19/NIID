#!/bin/env python3
import sys
import re
import pandas as pd

fil=sys.argv[1]
save=fil.split("/")[-1][:-4]

#fungi_28S
sent=sys.argv[2]
#out=sys.argv[3]


df2={}
c=0
with open(fil,"r") as Out:
    for x in Out:
        if re.search(sent,x):
            line=x.split()
            
            contig=line[2]
            start=int(line[-7])
            end=int(line[-8])
            strand=line[8]
            bit=float(line[3])

            if start > end:
                temp=[start,end]
                start=temp[1]
                end=temp[0]
            
            length=end-start
            
            name=f"{contig}:{start}-{end}"
            print(f"{name},{strand},{length}")
            df2[0]=[bit,length,name]
            c+=1

#df3= pd.DataFrame.from_dict(df2, orient='index',columns=["Bit Score","Length","Name"])

#temp1=df3.sort_values("Bit Score",ascending=False)
#temp1.to_csv(f"{out}/{save}_bit.csv",index=False)
#temp1=df3.sort_values("Length",ascending=False)
#temp1.to_csv(f"{out}/{save}_length.csv",index=False)


