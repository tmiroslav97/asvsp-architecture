#!/usr/bin/python

import sys

def remove_commas(word):
    while word and not word[0].isalpha():
        word = word[1:]
    while word and not word[-1].isalpha():
        word = word[:-1]
    
    return word.lower()

for myline in sys.stdin:
    line = myline.strip().split()

    for first in line:
        for second in line:
            f = remove_commas(first)
            s = remove_commas(second)
            if not f or not s or f == s:
                continue
            print("{} {} {}".format(f, s, 1))
