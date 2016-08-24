# encoding: utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import json


# 输入: url \t query = XXX \t {}, {} ..
# http://baike.baidu.com/view/4996.htm    query = 梁朝伟  {  name : 梁朝伟  formal : NULL  offset : 0  etype : 1009  type_confidence : 10  eid : 653fbe5a7e93489db56984c43754b277  entity_confidence : 10  }
# 输出: url \t [{}, {}]

def main(fin):

    for line in fin:
        line_list = line.strip().split("\t")
        if len(line_list) == 2:
            url = line_list[0].strip()
            ner_list = []
            print "%s\t%s" % (url, json.dumps(ner_list, ensure_ascii=False))

        else:

            url = line_list[0].strip()
            sentence = line_list[1].strip()
            sentence = sentence.replace("query =", "").strip()

            ner_list = []
            for s in line_list[2:]:
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

                        sentence = unicode(sentence)
                        dict_to_real_offset = {}
                        offset = 0
                        for i in range(len(sentence)):
                            dict_to_real_offset[offset] = i
                            if is_chinese(sentence[i]):
                                offset += 2
                            else:
                                offset += 1

                        if v in dict_to_real_offset:
                            v = dict_to_real_offset[v]

                    d[k] = v

                ner_list.append(d)

            print u"%s\t%s" % (url, json.dumps(ner_list, ensure_ascii=False))

def is_chinese(ch):
    if ord(ch) < 127:
        return False
    else:
        return True

if __name__ == '__main__':
    main(sys.stdin)


