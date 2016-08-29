#!python/bin/python
# encoding: utf-8
import json
import sys
import bs4
reload(sys)
sys.setdefaultencoding('utf-8')
from bs4 import BeautifulSoup
import sys, hashlib


# 输入url, 判断是不是 下载页
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
    x, o, confidence = is_xiazai(url, dict_info, soup)
    if x:
        S = get_s(url, dict_info, soup)
        P = u"下载"
        O = o

        print u"%s\t%s\t%s\t%s\t%.4f" % (url, S, P, O, confidence)


def is_xiazai(url, dict_info, soup):

    if soup is None:
        return (False, "~", 0)

    flag, o = has_download_a_tag_1(soup)
    if flag:
        return (True, o, 0.8)

    flag, o = has_download_a_tag_2(soup)
    if flag:
        return (True, o, 0.7)

    return (False, "~", 0)


# 1. 正文中, 下载被<a>包围, 至少得有href/onclick/id属性 且href指向的不是html
def has_download_a_tag_1(soup):

    for content in soup.find_all(attrs={"style": "border:3px solid red;overflow-y:auto;overflow-x:auto;"}):
        for a_tag in content.find_all("a"):
            if "下载" in "\t".join(a_tag.stripped_strings):
                # 至少得有这些标签之一
                if set(map(lambda x: x.lower(), a_tag.attrs.keys())) & {"href", "onclick", "id"}:
                    # 如果有href,指向的不能是html, htm
                    if "href" in a_tag.attrs:
                        if not a_tag.attrs["href"].endswith("htm") \
                            and not a_tag.attrs["href"].endswith("html")\
                            and not a_tag.attrs["href"].endswith("com")\
                            and not a_tag.attrs["href"].endswith("cn")\
                            and not a_tag.attrs["href"].endswith("php")\
                            and not a_tag.attrs["href"].endswith("jsp")\
                            and not a_tag.attrs["href"].endswith("/"):

                            # o 为下载链接
                            o = get_o(a_tag)
                            return True, o
                        else:
                            continue
                    return True, "~"
    return False, "~"


# 如果1.不成立, 对于满足要求的<a>, 判断周围是不是有 下载 关键字
def has_download_a_tag_2(soup):
    for content in soup.find_all(attrs={"style": "border:3px solid red;overflow-y:auto;overflow-x:auto;"}):
        for a_tag in content.find_all("a"):
            # 至少得有这些标签之一
            if set(map(lambda x: x.lower(), a_tag.attrs.keys())) & {"href", "onclick", "id"}:
                # 如果有href,指向的不能是html, htm
                flag = 1
                if "href" in a_tag.attrs:
                    if not a_tag.attrs["href"].endswith("htm") \
                            and not a_tag.attrs["href"].endswith("html")\
                            and not a_tag.attrs["href"].endswith("com")\
                            and not a_tag.attrs["href"].endswith("cn")\
                            and not a_tag.attrs["href"].endswith("php")\
                            and not a_tag.attrs["href"].endswith("jsp")\
                            and not a_tag.attrs["href"].endswith("/"):
                        pass
                    else:
                        flag = 0

                if flag == 1:

                    ''' 1. <a> 下面是否有 img 标签, 并且 alt 有 下载'''
                    for img in a_tag.find_all("img"):
                        if "alt" in img.attrs and "下载" in img.attrs["alt"]:
                            # o 为下载链接
                            o = get_o(a_tag)
                            return True, o


                    ''' 2. 周围的文字 '''
                    if a_tag.parent.name == "p":
                        a_tag = a_tag.parent

                    # <a> 周围的文字
                    surrounding_string = ""

                    for sibling in list(a_tag.previous_siblings):
                        if isinstance(sibling, bs4.element.NavigableString):
                            surrounding_string += str(sibling).strip()
                        else:
                            if sibling.name in ["span", "p", "b", "font"]:
                                for x in sibling.stripped_strings:
                                    surrounding_string += x

                    for sibling in list(a_tag.next_siblings):
                        if isinstance(sibling, bs4.element.NavigableString):
                            surrounding_string += str(sibling).strip()
                        else:
                            if sibling.name in ["span", "p", "b", "font"]:
                                for x in sibling.stripped_strings:
                                    surrounding_string += x
                    #

                    key_words = [
                        "下载地址",
                        "下载链接",
                        "链接下载",
                        "迅雷连接",
                        "迅雷链接",
                        "磁力链接",
                        "磁力连接",
                    ]

                    for word in key_words:
                        if word in surrounding_string:
                            o = get_o(a_tag)
                            return True, o
    return False, "~"



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

    # 如果有 【南妹皇后】, 《斗破苍穹》 取中间的
    if u"《" in title and u"》" in title:
        start = title.find(u"《")
        end = title.find(u"》")
        if start < end:
            title = title[start + 1: end]

    # 删除一些不必要的词
    useless_words = [
        u"txt",
        u"TXT",
        u"下载"
    ]

    for word in useless_words:
        if word in title:
            title = title.replace(word, "")

    return title




def get_o(a_tag):
    o = "~"
    if "href" in a_tag.attrs:
        o = a_tag.attrs["href"]
        if not o.startswith("http"):
            o = "~"
    return o



if __name__ == '__main__':
    main()
