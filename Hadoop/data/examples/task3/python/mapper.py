#!/usr/bin/python

import sys

for myline in sys.stdin:
    line = myline.strip().split(":")
    first = line[0]
    for second in line[1].split(","):
        if first < second:
            print("{},{}:{}".format(first, second, line[1]))
        else:
            print("{},{}:{}".format(second, first, line[1]))
