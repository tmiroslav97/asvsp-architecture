#!/usr/bin/python

import sys

def remove_commas(word):
    while word and not word[0].isalpha():
        word = word[1:]
    while word and not word[-1].isalpha():
        word = word[:-1]
    
    return word.lower()

def dict_to_string(h):
    return "@".join(['%s$%d' % (key, value) for (key, value) in h.items()])

for myline in sys.stdin:
    line = myline.strip().split()

    for first in line:
        f = remove_commas(first)
        if not f:
            continue

        h = {}
        for second in line:
            s = remove_commas(second)
            if not s or s == f:
                continue
            if s in h:
                h[s] += 1
            else:
                h[s] = 1

        print("{}#{}".format(f, dict_to_string(h)))