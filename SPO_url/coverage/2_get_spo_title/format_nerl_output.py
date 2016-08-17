# encoding: utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import json

def main(fin):

    for line in fin:
        line_list = line.strip().split("\t")

        if len(line_list) == 1:
            sentence = line_list[0].strip()
            sentence = sentence.replace("query =", "")
            ner_list = []

            print "%s\t%s" % (sentence, json.dumps(ner_list, ensure_ascii=False))

        else:
            sentence = line_list[0].strip()
            sentence = sentence.replace("query =", "")

            ner_list = []
            for s in line_list[1:]:
                # {  name : 春节  formal : 2016-02-08  offset : 0  etype : [D:TIME]  type_confidence : 5  eid :   entity_confidence : 0  }
                d = {}
                s = s[1:-1].strip()
                for x in s.split("  "):
                    print x, x.split(" : ", 1)
                    k, v = x.split(" : ", 1)
                    d[k] = v
                ner_list.append(d)

            print "%s\t%s" % (sentence, json.dumps(ner_list, ensure_ascii=False))


if __name__ == '__main__':
    main(sys.stdin)


