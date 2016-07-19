#!usr/bin/env python
# coding: utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import json

def do_so_count(in_file):

    count = {}

    with open(in_file) as fin:
        for line in fin:
            d = json.loads(line)
            for P in d["mars_ner"]:

                if P not in count:
                    count[P] = 0

                s_list = d["mars_ner"][P]["s"]
                o_list = d["mars_ner"][P]["o"]

                if s_list != [] and o_list != []:
                    count[P] += 1

    for P in count:
        print P, count[P]

if __name__ == '__main__':
    in_file = sys.argv[1]
    do_so_count(in_file)