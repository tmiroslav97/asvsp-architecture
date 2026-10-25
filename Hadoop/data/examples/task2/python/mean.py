#!/usr/bin/env python3
import sys

for line in sys.stdin:
    fields = line.rstrip("\n").split("\t")
    if len(fields) == 2:
        print(float(fields[0]) / int(fields[1]))
