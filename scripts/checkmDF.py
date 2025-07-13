import sys
import re

with open(sys.argv[1],"r") as check:
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
header=",".join(header)
values=",".join(values)

print(values)
