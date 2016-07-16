#!tools/python/bin/python
# coding: utf-8
import json
import uuid
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

# 致获取具体P相关的数据
def main(P_wanted):
    for line in sys.stdin:
        line = line.strip()
        dict_SO = eval(line.split("\t")[-1])

        t = {}

        s, o = dict_SO[P_wanted]["s"], dict_SO[P_wanted]["o"]
        if s != [] and o != []:
            # 个数大于5的不要了,与tutorial一致
            if len(s) > 5 or len(o) > 5:
                continue
            t[P_wanted] = dict_SO[P_wanted]
            new_line = "\t".join(line.split("\t")[:-1]) + "\t" + json.dumps(t, ensure_ascii=False)
            print new_line

if __name__ == '__main__':

    P_wanted = sys.argv[1]
    main(P_wanted)