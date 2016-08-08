#!python/bin/python
#  encoding: utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

for line in sys.stdin:
    url = line.split("\t")[0]
    url = unicode(url, errors="ignore")
    print url