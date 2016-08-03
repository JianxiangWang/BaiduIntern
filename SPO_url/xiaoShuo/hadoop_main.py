#!python/bin/python
# encoding: utf-8
import json
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import sys

# 输入url, 判断是不是 小说
def main():

    for line in sys.stdin:
        line_list = line.strip().split("\t")
        url = line_list[0]
        dict_info = json.loads(line_list[-1])

        if is_xiaoShuo(url, dict_info):
            title = dict_info["realtitle"]
            S = title
            P = "体裁/小说"
            O = url

            print "%s\t%s\t%s\t%s" % (url, S, P, O)


def is_xiaoShuo(url, dict_info):

    page_type_list = dict_info["page_type"]
    if {"小说首页", "小说列表页"} & set(page_type_list):
        return True
    else:
        return False



if __name__ == '__main__':
    main()
