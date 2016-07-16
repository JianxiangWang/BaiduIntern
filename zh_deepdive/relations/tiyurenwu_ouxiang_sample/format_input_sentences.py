# coding: utf-8
import random
import re
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def main(in_file, to_file, fraction):
    fin = open(in_file)
    fout = open(to_file, "w")

    index = 0
    for line in fin:
        line_list = line.strip().split("\t")
        line_list[2] = line_list[2].replace("\"", "'")
        line_list[2] = "{" + line_list[2][1:-1].replace("{", "《").replace("}", "》") +"}"

        if line_list[2] == "{}":
            continue

        if index % 10 == 0:
            fout.write("\t".join(line_list) + "\n")

        index += 1




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

    main("input/tiyurenwu_ouxiang.part10", "input/sentences.new.0.1.tsv", fraction=0.1)