#!/usr/bin/env python3

import sys

total = 0.0
count = 0

for line in sys.stdin:
    fields = line.rstrip("\n").split("\t")
    if len(fields) != 2:
        continue
    try:
        total += float(fields[0])
        count += int(fields[1])
    except ValueError:
        continue

print(f"{total}\t{count}")
