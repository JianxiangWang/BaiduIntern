#!python/bin/python
#  encoding: utf-8
import json
import sys

from bs4 import BeautifulSoup

reload(sys)
sys.setdefaultencoding('utf-8')
import sys


# 输入url, 判断是不是 视频
def main(fin):
    for line in fin:

        line_list = line.strip().split("\t")
        url = line_list[0]
        dict_info = json.loads(line_list[-1])

        try:
            soup = BeautifulSoup(dict_info["cont_html"], "html.parser")
        except:
            soup = None

        do_extraction(url, dict_info, soup)


def do_extraction(url, dict_info, soup):

    x, confidence = is_shipin(url, dict_info, soup)
    if x:
        S = get_s(url, dict_info, soup)
        P = u"视频"
        O = url

        print u"%s\t%s\t%s\t%s\t%.4f" % (url, S, P, O, confidence)


def is_shipin(url, dict_info, soup):

    page_type_list = dict_info["page_type"]

    if {u"视频播放页"} & set(page_type_list):
        return (True, 1)
    else:
        return (False, 0)


# 视频
def get_s(url, dict_info, soup):
    ner_list = dict_info["title_ner"]
    title = dict_info['realtitle']
    if ner_list != []:
        before_idx = len(title)
        entity_name = None

        for ner in ner_list:
            offset = ner["offset"]
            etype = ner["etype"]

            if offset < before_idx:
                entity_name = ner["name"]

        if entity_name:
            title = entity_name

    if u"【" in title and u"】" in title:
        start = title.find(u"【")
        end = title.find(u"】")
        if start < end:
            title = title[start + 1: end]

    # 用去掉一些词
    useless_end_words = [
        u"的视频",
        u"短视频",
        u"热门视频",
        u"爆笑视频",
        u"搞笑视频",
        u"视频",
    ]
    useless_start_words = [
        u"视频:",
        u"精选"
    ]


    for end_word in useless_end_words:
        if title.endswith(end_word):
            title = title[:len(title) - len(end_word)]

    for start_word in useless_start_words:
        if title.startswith(start_word):
            title = title[len(start_word):]

    return title


if __name__ == '__main__':
    main(sys.stdin)
