#!python/bin/python
# encoding: utf-8
import json
import sys

from bs4 import BeautifulSoup

reload(sys)
sys.setdefaultencoding('utf-8')
import sys

# 输入url, 判断是不是 小说
def main():

    for line in sys.stdin:
        line_list = line.strip().split("\t")
        url = line_list[0]
        dict_info = json.loads(line_list[-1])

        try:
            soup = BeautifulSoup(dict_info["cont_html"], "html.parser")
        except:
            soup = None

        do_extraction(url, dict_info, soup)


def do_extraction(url, dict_info, soup):
    x, confidence = is_xiaoShuo(url, dict_info, soup)
    if x:
        url = unicode(url, errors="ignore")
        S = get_s(url, dict_info, soup)
        P = u"小说"
        O = url

        print u"%s\t%s\t%s\t%s\t%.4f" % (url, S, P, O, confidence)

def is_xiaoShuo(url, dict_info, soup):

    page_type_list = dict_info["page_type"]
    if {u"小说首页", u"小说列表页"} & set(page_type_list):
        return (True, 1)
    else:
        return (False, 0)


def get_s(url, dict_info, soup):
    # 1. 如果title中有《》,将《》里面的内容作为s
    title  = dict_info["realtitle"]
    if u"《" in title and u"》" in title:
        s = title.find(u"《")
        e = title.find(u"》")
        if s < e:
            return remove_flanking_symbols(title[s+1: e])

    # 2. 删除一些无用的词
    useless_words = [
        u"最新章节列表",
        u"简介",
        u"txt",
        u"免费",
        u"全文",
        u"阅读",
        u"最新章节",
        u"更新列表",
        u"TXT",
        u"全集",
        u"下载"
    ]
    for word in useless_words:
        title = title.replace(word, "")

    return remove_flanking_symbols(title)


def remove_flanking_symbols(str):

    en_punctuations = u""" !"#&'*+,-..../:;<=>?@[\]^_`|%""" + "``" + "''"
    ch_punctuations = u"``''，。；、：？！∶… …──“”＊「」《》【】"
    nums = u"0123456789"
    symbols = en_punctuations + ch_punctuations + nums
    return _remove_flanking_symbols(str, symbols)



def _remove_flanking_symbols(string, symbols):
    i = 0
    while i < len(string) and (string[i] in symbols):
        i += 1
    if i == len(string):
        return ""

    j = len(string) - 1
    while j >= 0 and (string[j] in symbols):
        j -= 1
    return string[i: j + 1]

if __name__ == '__main__':
    main()
