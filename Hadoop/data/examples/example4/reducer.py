#!/usr/bin/python
import sys 

current_type = ""
current_amount = 0
payment_type = ""
amount = 0

for line in sys.stdin: 
    line = line.strip()
    tokens = line.split(',')
    payment_type = tokens[0]
    amount = tokens[1]
    try: 
        amount = int(amount) 
    except ValueError:
        continue
    if current_type == payment_type: 
        current_amount += amount 
    else: 
        if current_type:
            print ('%s\t%s' % (current_type, current_amount))
        current_amount = amount
        current_type = payment_type

if current_type == payment_type: 
    print ('%s\t%s' % (current_type, current_amount))