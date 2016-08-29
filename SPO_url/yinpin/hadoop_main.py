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

        try:
            soup = BeautifulSoup(dict_info["cont_html"], "html.parser")
        except:
            soup = None
        do_extraction(url, dict_info, soup)


def do_extraction(url, dict_info, soup):

    x, confidence = is_yinpin(url, dict_info, soup)
    if x:
        S = get_s(url, dict_info, soup)
        P = u"音频"
        O = url

        print u"%s\t%s\t%s\t%s\t%.4f" % (url, S, P, O, confidence)


def is_yinpin(url, dict_info, soup):

    if soup  is None:
        return (False, 0)

    # 基于meta的识别
    content = get_meta_content(soup)

    flag = 0
    keywords = ["音乐", "播放器", "电台", "歌曲"]
    for keyword in keywords:
        if keyword in content or (soup.title != None and soup.title.string != None and keyword in soup.title.string):
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
                break

        if entity_name:
            title = entity_name

    return title


if __name__ == '__main__':
    main()
