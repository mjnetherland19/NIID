import sys
import pandas as pd

df=pd.read_csv(sys.argv[1],sep="\t",names=["Reference","Query","Distance","P-value","Hashes"])
num=int(sys.argv[2])
save=sys.argv[3]
df=df.sort_values("Distance")
if num == 1:
    df.to_csv(f"{save}_mash.csv",index=False)
else:
    df=df.iloc[0:num]
    df.to_csv(f"{save}_mash.csv",index=False)
