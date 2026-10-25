#!/usr/bin/env python3

import sys
import os

MEAN = float(os.environ["MEAN"])

for myline in sys.stdin:
    columns = myline.strip().split(",")
    sqdif = (float(columns[1]) - MEAN)**2
    print('%s\t%s' % (sqdif, 1))
