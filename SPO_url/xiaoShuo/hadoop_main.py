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

        do_extraction(url, dict_info, line_list[-1])


def do_extraction(url, dict_info, str_info):
    x, confidence = is_xiaoShuo(url, dict_info)
    if x:
        url = unicode(url, errors="ignore")
        title = dict_info["realtitle"]
        S = title
        P = u"体裁/小说"
        O = url

        print u"%s\t%s\t%s\t%s\t%.4f\t%s" % (url, S, P, O, confidence, str_info)

def is_xiaoShuo(url, dict_info):

    page_type_list = dict_info["page_type"]
    if {u"小说首页", u"小说列表页"} & set(page_type_list):
        return (True, 1)
    else:
        return (False, 0)


if __name__ == '__main__':
    main()
