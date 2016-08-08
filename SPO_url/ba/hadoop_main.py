#!python/bin/python
# encoding: utf-8
import json
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import sys


# 输入url, 判断是不是 贴吧
def main(fin):
    for line in fin:
        line_list = line.strip().split("\t")
        url = line_list[0]
        dict_info = json.loads(line_list[-1])

        do_extraction(url, dict_info)


def do_extraction(url, dict_info):
    x, confidence = is_ba(url, dict_info)
    if x:
        url = unicode(url, errors="ignore")
        title = dict_info["realtitle"]
        S = title
        P = u"吧"
        O = url

        print u"%s\t%s\t%s\t%s\t%.4f" % (url, S, P, O, confidence)


def is_ba(url, dict_info):

    # # 首先, 域名过滤
    # if "tieba.baidu.com" not in url:
    #     return (False, 0)


    page_type_list = dict_info["page_type"]
    if {u"论坛帖子页"} & set(page_type_list):
        return (True, 1)
    else:
        return (False, 0)


if __name__ == '__main__':
    main(sys.stdin)
