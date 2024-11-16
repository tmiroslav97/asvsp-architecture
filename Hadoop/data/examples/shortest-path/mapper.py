#!/usr/bin/python

import sys

for line in sys.stdin:
    line = line.strip()
    tokens = line.split(" ")
    
    node = tokens[0]
    path = tokens[1]
    dist = -1
    try:
        dist = int(tokens[2])
    except:
        continue

    print ("%s %s" % (node, line))

    if dist != -1:
        for neigh in tokens[3:]:
            print ("%s %d %s" % (neigh, dist+1, node + ":" + path))

    