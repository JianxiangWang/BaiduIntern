# coding: utf-8
import json
import random
import re
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def main(in_file, to_file, fraction):
    fin = open(in_file)
    fout = open(to_file, "w")

    for line in fin:
        line_list = line.strip().split("\t")
        line_list[2] = line_list[2].replace("\"", "'")
        line_list[2] = "{" + line_list[2][1:-1].replace("{", "《").replace("}", "》") +"}"

        if line_list[2] == "{}":
            continue

        # 过滤只有一个人的
        dict_so = json.loads(line_list[-1])
        so_sets = set([])
        for P in dict_so:
            s_list, o_list = dict_so[P]["s"], dict_so[P]["o"],
            for so_mention, _, char_start_index, length in s_list + o_list:
                so_sets.add((so_mention, char_start_index, length))

        if len(so_sets) <= 1 or len(so_sets) >= 5:
            continue

        if fraction == 1:
            fout.write("\t".join(line_list) + "\n")
        elif decide(fraction=fraction):
            fout.write("\t".join(line_list) + "\n")

    fin.close()
    fout.close()


def decide(fraction):
    # [0, 1)
    dice = random.random()
    if dice < fraction:
        return True
    else:
        return False


if __name__ == '__main__':

    main("input/tiyurenwu_ouxiang.part10", "input/sentences.new.0.5.tsv", fraction=0.5)