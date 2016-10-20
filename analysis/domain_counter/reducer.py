#!python/bin/python
#encoding: utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


# counter = {}
for line in sys.stdin:
    print line
#     domain, _ = line.strip().split("\t")
#     if domain not in counter:
#         counter[domain] = 0
#     counter[domain] += 1
#
# for domain in counter:
#     print "%s\t%d" % (domain, counter[domain])


