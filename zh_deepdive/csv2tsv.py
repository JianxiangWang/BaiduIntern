#!/usr/bin/env python
import sys,csv
for row in csv.reader(sys.stdin):
  print "\t".join(row)