#!/usr/bin/env python3
import sys

for line in sys.stdin:
    fields = line.rstrip("\n").split(",")
    if len(fields) < 2:
        continue
    try:
        print(f"{float(fields[1])}\t1")
    except ValueError:
        continue
