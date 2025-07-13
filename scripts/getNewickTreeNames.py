#!/bin/env python3
import sys
import re

prog = re.compile("(?<=,)[A-Za-z].+?(?=:)|(?<=\()[A-Za-z].+?(?=:)|(?<=\()[0-9].+?(?=:)|(?<=,)[0-9].+?(?=:)")
#result = prog.match(string)

out=sys.argv[2]
with open(sys.argv[1],"r") as tree:
	F=tree.readline().strip()
#names=re.findall("[A-Z].+?(?=:)",F)
names=prog.findall(F)
with open(out,"w") as pars:
    for x in names:
        pars.write(f"{x}\n")
