#!/usr/bin/python

import sys

for myline in sys.stdin:
    columns = myline.strip().split(",")
    print('%s\t%s' % (columns[1], 1))
