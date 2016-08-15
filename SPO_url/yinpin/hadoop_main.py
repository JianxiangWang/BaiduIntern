#!python/bin/python
# encoding: utf-8
import json
import sys

import re

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

        # 1. 判断是否存在audio标签
        x = 0
        for audio in soup.find_all("audio"):
            if "src" in audio.attrs and audio.attrs["src"].endswith(".mp3"):
                return (True, 0.9)
            x = 1
        if x == 1:
            return (True, 0.6)

        # 2. 判断页面是否有播放元素
        if soup.find(play_button):
            return (True, 0.8)


    return (False, 0)


def play_button(tag):

    if tag.name in ["a", "button"]:

        if "title" in tag.attrs:
            title = tag.attrs["title"]
            filter_words = ["播放记录", "播放时间"]
            for word in filter_words:
                if word in title:
                    return False

            if title.startswith("播放"):
                return True
        if "id" in tag.attrs:
            id_ = tag.attrs["id"]
            if id_ == "play":
                return True

    return False



def get_meta_content(soup):
    content = ""
    for meta in soup.find_all("meta"):
        if "content" in meta.attrs:
            content += meta["content"] + "\t"
    return content.strip()


if __name__ == '__main__':
    main()
