#!python/bin/python
# encoding: utf-8
import json
import sys
import bs4
import re
from bs4 import BeautifulSoup
reload(sys)
sys.setdefaultencoding('utf-8')
import sys


# 输入url, 判断是不是 图片
def main():
    for line in sys.stdin:
        line_list = line.strip().split("\t")
        url = line_list[0]
        dict_info = json.loads(line_list[-1])

        do_extraction(url, dict_info)


def do_extraction(url, dict_info):
    x, confidence = is_tupian(url, dict_info)
    if x:
        title = dict_info["realtitle"]
        S = title
        P = u"图片"
        O = unicode(url, errors="ignore")

        print u"%s\t%s\t%s\t%s\t%.4f" % (url, S, P, O, confidence)



def is_tupian(url, dict_info):
    soup = BeautifulSoup(dict_info["cont_html"], "html.parser")

    #
    images, content_string = get_all_images_and_content_string(soup)

    # 先获取满足大小的
    satisfied_images = []
    for image in images:
        flag = 0
        if "style" in image.attrs:
            dict_style = style_to_dict(image["style"])
            if "height" in dict_style and "width" in dict_style:
                flag = 1
                try:
                    height = int(dict_style["height"].lower().replace("px", ""))
                    width = int(dict_style["width"].lower().replace("px", ""))
                    if height > 300 and width > 200:
                        satisfied_images.append(image)
                except:
                    continue


        # 没找到去 width="500" height="375"
        if flag == 0:
            if "height" in image.attrs and "width" in image.attrs:
                try:
                    height = int(image["height"].lower().replace("px", ""))
                    width = int(image["width"].lower().replace("px", ""))
                    if height > 300 and width > 200:
                        satisfied_images.append(image)
                except:
                    continue

    if sum([_get_image_position(url, soup, image) for image in satisfied_images[:2]]) >= 1:
        # 文字与满足大小的图片的比例
        rate = len(content_string) / len(satisfied_images)
        if rate > 1000:
            return (False, 0)
        else:
            return (True, 1)
    else:

        # 没有满足条件, 获取所有的前50%图片的位置,判断是不是都在页面的上半部分
        image_num = len(images)

        # 图片数量小于3的, 直接不考虑
        if image_num < 3:
            return (False, 0)
        # 必须全部在上面
        if image_num >= 3 and image_num <=5:
            if sum([_get_image_position(url, soup, image) for image in images]) == image_num:
                return (True, 0.8)
            else:
                return (False, 0)
        # 图片数量大于5的
        if sum([_get_image_position(url, soup, image) for image in images[:len(images)/2]]) == len(images)/2:
            return (True, 0.7)
        else:
            return (False, 0)



def get_all_images_and_content_string(soup):
    content_string = ""
    images = []
    for content in soup.find_all(attrs={"style": "border:3px solid red;overflow-y:auto;overflow-x:auto;"})[:3]:
        for img in content.find_all("img"):
            images.append(img)

        for s in content.stripped_strings:
            content_string += s

    return images, content_string


# 1: 在页面的前半部分
# 0: 在页面的后半部分
def _get_image_position(url, soup, img):

    # 对于贴吧特殊处理
    if "tieba.baidu.com" in url:
        j_p_postlist = soup.find(id="j_p_postlist") # 直接对应到到用户发的帖子
        return _tag_to_parent_position(img, j_p_postlist)

    # http://sh.xinhuanet.com/
    if "sh.xinhuanet.com" in url:
        myTable = soup.find(id="myTable")
        if myTable:
            if myTable in img.parents:
                return 1
            else:
                return 0

    if soup.find("div", id="center"):
        return _tag_to_parent_position(img, soup.find(id="center"))

    if soup.find("div", class_="article"):
        return _tag_to_parent_position(img, soup.find("div", class_="article"))

    if soup.find("div", class_=re.compile('''.*content.*''')):
        return _tag_to_parent_position(img, soup.find("div", class_=re.compile('''.*content.*''')))

    return _tag_to_parent_position(img, soup.find("body"))


# tag 到 父节点的位置
def _tag_to_parent_position(tag, parent):

    if parent not in tag.parents:
        return 0

    x = tag
    while x.parent != parent:
        x = x.parent

    parent_children = []
    for child in parent.contents:
        if isinstance(child, bs4.element.NavigableString):
            continue
        if child.name == "script":
            continue
        parent_children.append(child)

    if (parent_children.index(x) - 1) / float(len(parent_children)) <= 0.5:
        return 1

    return 0


# float:right; height:403px; width:267px
def style_to_dict(style):
    d = {}
    for item in style.split(";"):
        try:
            key, value = item.strip().split(":")
            d[key.strip().lower()] = value.strip().lower()
        except:
            continue
    return d


if __name__ == '__main__':
    main()
