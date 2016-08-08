#!python/bin/python
#  encoding: utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from itertools import groupby

for key, group in groupby(sys.stdin, key=lambda x: x.strip()):
    for line in group:
        print line
        break