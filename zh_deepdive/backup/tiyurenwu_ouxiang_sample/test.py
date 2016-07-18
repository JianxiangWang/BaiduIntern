# coding: utf-8
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

dict_P_to_so_set = {}
fin = open("../../data/out.txt")
lines = fin.readlines()
fin.close()

index = 0
for line in lines:
    # this_P, this_num, this_so_set = line.strip().split("\t")
    # this_so_set = eval(this_so_set)
    # dict_P_to_so_set[this_P] = this_so_set
    this_P, this_num, s = line.strip().split("\t")
    this_so_set = eval(s)

    # print type(s), type(this_so_set)

    # print this_so_set

    # index += 1
    # if index == 2:
    #     break

    # break
    pass