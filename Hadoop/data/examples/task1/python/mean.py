#!/usr/bin/python

import sys

for myline in sys.stdin:
    columns = myline.strip().split("\t")
    sum = float(columns[0])
    count = int(columns[1])
    print(sum/count)
