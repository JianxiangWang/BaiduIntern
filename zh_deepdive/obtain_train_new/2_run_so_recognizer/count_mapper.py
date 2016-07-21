#!tools/python/bin/python
# coding: utf-8
import json
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def main():
    for line in sys.stdin:
        d = json.loads(line)

        for P in d["mars_ner"]:
            s_list = d["mars_ner"][P]["s"]
            o_list = d["mars_ner"][P]["o"]
            if s_list != [] and o_list != []:
                print "%s\t%d" % (P, 1)

if __name__ == '__main__':
    main()