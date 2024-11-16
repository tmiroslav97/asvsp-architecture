#!/usr/bin/python

import sys

current_pair = ""
current_count = 0

for myline in sys.stdin:
    first, second, count = myline.strip().split()
    count = int(count)
    pair = [first, second]

    if current_pair == pair:
        current_count += count
    else:
        if current_pair:
            print("{} {} {}".format(current_pair[0], current_pair[1], current_count))
        current_pair = pair
        current_count = count

if current_pair == pair:
    print("{} {} {}".format(current_pair[0], current_pair[1], current_count))
