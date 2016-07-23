# encoding: utf-8

import json


# 统计一下, so 全部为 []的个数
def main(in_file):

    count = 0

    for line in open(in_file):
        line = json.loads(line)

        flag = 0
        for P in line["mars_ner"]:
            s_list, o_list = line["mars_ner"][P]["s"], line["mars_ner"][P]["o"]

            # 不为空
            if s_list != [] and o_list != []:
                flag = 1

        if flag == 0:
            count += 1

    print count

if __name__ == '__main__':
    main("part-00000")
