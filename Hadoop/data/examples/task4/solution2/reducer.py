#!/usr/bin/python

import sys

current_word = ""
current_h = {}

for myline in sys.stdin:
    try:
        word, rest = myline.strip().split("#")
    except:
        continue
    
    h = {}
    for i in rest.split("@"):
        try:
            key, value = i.split("$")
            h[key] = int(value)
        except:
            continue

    if current_word == word:
        for key in h:
            if key in current_h:
                current_h[key] += h[key]
            else:
                current_h[key] = h[key]
    else:
        if current_word:
            for key in current_h:
                print("{} {} {}".format(current_word, key, current_h[key]))
        current_word = word
        current_h = h

if current_word == word:
    for key in current_h:
        print("{} {} {}".format(word, key, current_h[key]))
