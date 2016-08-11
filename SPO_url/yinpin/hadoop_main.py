#!python/bin/python
# encoding: utf-8
import json
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from bs4 import BeautifulSoup
import sys, hashlib


# 输入url, 判断是不是 音频页
def main():

    for line in sys.stdin:
        line_list = line.strip().split("\t")
        url = line_list[0]
        dict_info = json.loads(line_list[-1])

        do_extraction(url, dict_info, line_list[-1])


def do_extraction(url, dict_info, str_info):

    x, confidence = is_yinpin(url, dict_info)
    if x:
        url = unicode(url, errors="ignore")
        title = dict_info["realtitle"]
        S = title
        P = u"音频"
        O = url

        print u"%s\t%s\t%s\t%s\t%.4f" % (url, S, P, O, confidence)


def is_yinpin(url, dict_info):

    try:
        soup = BeautifulSoup(dict_info["cont_html"], "html.parser")
    except:
        return (False, 0)

    # 基于meta的识别
    content = get_meta_content(soup)

    flag = 0
    keywords = ["音乐", "播放器", "电台", "歌曲"]
    for keyword in keywords:
        if keyword in content or keyword in soup.title.string:
            flag = 1

    if flag == 1:
        # 判断页面是否有播放元素
        if len(soup.find_all("a", attrs={"title": "播放"})) > 0:
            return (True, 0.8)

    return (False, 0)


def get_meta_content(soup):
    content = ""
    for meta in soup.find_all("meta"):
        if "content" in meta.attrs:
            content += meta["content"] + "\t"
    return content.strip()


if __name__ == '__main__':
    main()
