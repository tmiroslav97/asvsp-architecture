#!/usr/bin/python
import sys

amount = 0

for line in sys.stdin:
    line = line.strip()
    words = line.split(",")
    payment_type = words[3]
    try:
        amount = int(words[2])
    except:
        continue
    print ('%s,%d' % (payment_type, amount))
