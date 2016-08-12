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

        do_extraction(url, dict_info, line_list[-1])


def do_extraction(url, dict_info, str_info):
    x, confidence = is_xiazai(url, dict_info)
    if x:
        url = unicode(url, errors="ignore")
        title = dict_info["realtitle"]
        S = title
        P = u"下载"
        O = url

        print u"%s\t%s\t%s\t%s\t%.4f" % (url, S, P, O, confidence)


def is_xiazai(url, dict_info):

    try:
        soup = BeautifulSoup(dict_info["cont_html"], "html.parser")
    except:
        return (False, 0)

    if has_download_a_tag_1(soup):
        return (True, 0.8)

    if has_download_a_tag_2(soup):
        return (True, 0.7)

    return (False, 0)


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
                            and not a_tag.attrs["href"].endswith("/"):
                            return True
                        else:
                            continue
                    return True
    return False


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
                            and not a_tag.attrs["href"].endswith("/"):
                        pass
                    else:
                        flag = 0

                if flag == 1:

                    ''' 1. <a> 下面是否有 img 标签, 并且 alt 有 下载'''
                    for img in a_tag.find_all("img"):
                        if "alt" in img.attrs and " 下载" in img.attrs["alt"]:
                            return True


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
                    if "下载地址" in surrounding_string or "下载链接" in surrounding_string or "链接下载" in surrounding_string:
                        return True
    return False


if __name__ == '__main__':
    main()
