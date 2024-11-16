#!/usr/bin/python

import sys

sum = 0
count = 0

for myline in sys.stdin:
    words = myline.strip().split('\t')
    try:
        sum += float(words[0])
        count += int(words[1])
    except ValueError:
        continue

print('%s\t%s' % (sum, count))
