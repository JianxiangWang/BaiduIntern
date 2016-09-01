#!/usr/bin/env python
# encoding: utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import sys,csv
import re


for row in csv.reader(sys.stdin):
    new_row = []
    for x in row:
        x = x.strip()
        x = x.replace("\t", "")
        x = x.replace("\n", "")
        x = re.sub('\s+', ' ', x)
        new_row.append(x)

    print "\t".join(new_row)
