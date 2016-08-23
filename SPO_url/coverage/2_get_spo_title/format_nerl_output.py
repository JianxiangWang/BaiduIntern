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
                    k, v = x.split(" :", 1)
                    v = v.strip()

                    if k in ["type_confidence", "entity_confidence"]:
                        v = float(v)
                    if k in ["offset"]:
                        v = int(v)

                        # 需要重新计算offset
                        sentence = unicode(sentence)
                        dict_to_real_offset = {}
                        offset = 0
                        for i in range(len(sentence)):
                            dict_to_real_offset[offset] = i
                            if is_chinese(sentence[i]):
                                offset += 2
                            else:
                                offset += 1
                        v = dict_to_real_offset[v]

                    d[k] = v

                ner_list.append(d)

            print u"%s\t%s" % (sentence, json.dumps(ner_list, ensure_ascii=False))




def is_chinese(ch):
    if u'\u4e00' <= ch <= u'\u9fff':
        return True
    return False

if __name__ == '__main__':
    main(sys.stdin)


