#!tools/python/bin/python
# coding: utf-8
import json
import sys
from itertools import groupby
reload(sys)
sys.setdefaultencoding('utf-8')

def main():
    for key, lines in groupby(sys.stdin, key=lambda x: x.split("\t")[0]):

        c = 0
        # P\t1
        for line in lines:
            c += int(line.strip().split("\t")[-1])

        print "%s\t%d" % (key, c)


if __name__ == '__main__':
    main()