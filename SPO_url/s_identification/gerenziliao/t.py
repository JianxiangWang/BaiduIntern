# encoding: utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def main(P):
    for line in open("../1_get_all_urls/qiandaohu_10ku_spo"):
        line_list = line.strip().split("\t")
        this_P = line_list[2]
        if this_P == P:
            print line.strip()

if __name__ == '__main__':
    main("个人资料")