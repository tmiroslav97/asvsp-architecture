#!/usr/bin/python

import sys

current_pair = ""
current_set = set()
word = ""

for myline in sys.stdin:
    myline = myline.strip()
    pair, friends_set = myline.split(':')
    friends = friends_set.split(",")

    if current_pair == pair:
        current_set &= set(friends)
    else:
        if current_pair:
            print('%s:%s' % (current_pair, list(current_set)))
        current_pair = pair
        current_set = set(friends)

if current_pair == pair:
    print('%s:%s' % (current_pair, list(current_set)))
