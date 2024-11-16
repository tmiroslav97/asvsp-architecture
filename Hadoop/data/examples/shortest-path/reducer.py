#!/usr/bin/python

import sys

current_node = ""
current_dist = sys.maxint
current_path = ""
current_page = ""
path = "_"
dist = sys.maxint
is_node = True

for line in sys.stdin:
    line = line.strip()
    tokens = line.split(' ')

    node = tokens[0]

    try:
        path = tokens[2]
        dist = int(tokens[1])
        dist = sys.maxint if dist == -1 else dist
        is_node = True
    except ValueError:
        prev_page = None if is_node else page

        is_node = False
        page = tokens[2:]
        path = page[0]
        dist = int(page[1])
        dist = sys.maxint if dist == -1 else dist
    #print(is_node)
    if current_node == node:
        if dist < current_dist:
            current_dist = dist
            current_path = path     
    else:
        if current_node:
            #print(current_node, node, is_node)
            current_page = page if is_node else prev_page
            current_page[0] = current_path
            current_dist = -1 if current_dist == sys.maxint else current_dist
            current_page[1] = str(current_dist)

            print ("%s %s" % (current_node, " ".join(current_page)))

        current_node = node
        current_path = path
        current_dist = dist
        current_page = ""

if current_node == node:
    current_page = page
    current_page[0] = current_path
    current_dist = -1 if current_dist == sys.maxint else current_dist
    current_page[1] = str(current_dist)

    print ("%s %s" % (current_node, " ".join(current_page)))