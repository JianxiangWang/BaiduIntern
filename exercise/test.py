#!/usr/bin/env python
# coding: utf-8
import sys
reload(sys) 
sys.setdefaultencoding('utf-8')

fin1 = open("test.txt")
fin2 = open("test.txtDD")

for line1, line2 in zip(fin1, fin2):
    print line1, line2




