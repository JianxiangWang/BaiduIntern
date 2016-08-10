#!python/bin/python
#  encoding: utf-8
import json
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import sys


# 输入url, 判断是不是 视频
def main(fin):
    for line in fin:

        line_list = line.strip().split("\t")
        url = line_list[0]
        dict_info = json.loads(line_list[-1])

        do_extraction(url, dict_info, line_list[-1])


def do_extraction(url, dict_info, str_info):

    x, confidence = is_shipin(url, dict_info)
    if x:
        url = unicode(url, errors="ignore")
        title = dict_info["realtitle"]
        S = title
        P = u"视频"
        O = url

        print u"%s\t%s\t%s\t%s\t%.4f\t%s" % (url, S, P, O, confidence, str_info)


def is_shipin(url, dict_info):

    page_type_list = dict_info["page_type"]

    if {u"视频播放页"} & set(page_type_list):
        return (True, 1)
    else:
        return (False, 0)


if __name__ == '__main__':
    main(sys.stdin)
