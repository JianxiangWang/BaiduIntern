# coding: utf-8
import random
import re
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def main(in_file, to_file, fraction):
    fin = open(in_file)
    fout = open(to_file, "w")

    for line in fin:
        if decide(fraction):
            fout.write(line)

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

    main("/home/jianxiang/pycharmSpace/BaiduIntern/zh_deepdive/data/SPO_train_data_for_deepdive",
         "/home/jianxiang/pycharmSpace/BaiduIntern/zh_deepdive/data/SPO_train_data_for_deepdive_0.01",
         fraction=0.01
    )