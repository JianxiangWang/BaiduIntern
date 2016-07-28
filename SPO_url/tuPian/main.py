#!/usr/bin/env python
# encoding: utf-8
import sys

import bs4
import re
from bs4 import BeautifulSoup

reload(sys)
sys.setdefaultencoding('utf-8')
import subprocess
import sys, hashlib
import os


# 输入url, 判断是不是 图片
def main():
    for line in sys.stdin:
        url = line.strip()
        if is_tupian(url):
            title = get_url_title(url)
            S = title
            P = "图片"
            O = url

            print "%s\t%s\t%s\t%s" % (url, S, P, O)


def is_tupian(url):
    html_path = get_url_tagged_content_html_path(url)
    soup = BeautifulSoup(open(html_path), "html.parser")

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
                height = int(dict_style["height"].lower().replace("px", ""))
                width = int(dict_style["width"].lower().replace("px", ""))

                if height > 300 and width > 200:
                    satisfied_images.append(image)

        # 没找到去 width="500" height="375"
        if flag == 0:
            if "height" in image.attrs and "width" in image.attrs:
                height = int(image["height"].lower().replace("px", ""))
                width = int(image["width"].lower().replace("px", ""))
                if height > 300 and width > 200:
                    satisfied_images.append(image)

    print len(satisfied_images)

    if sum([_get_image_position(url, soup, image) for image in satisfied_images[:2]]) >= 1:

        # 文字与满足大小的图片的比例
        rate = len(content_string) / len(satisfied_images)
        print content_string
        print len(content_string), len(satisfied_images), len(content_string) / len(satisfied_images)

        return True
    else:

        # 没有满足条件, 获取所有的前50%图片的位置,判断是不是都在页面的上半部分
        image_num = len(images)

        # 图片数量小于3的, 直接不考虑
        if image_num < 3:
            return False
        # 必须全部在上面
        if image_num >= 3 and image_num <=5:
            if sum([_get_image_position(url, soup, image) for image in images]) == image_num:
                return True
            else:
                return False
        # 图片数量大于5的
        if sum([_get_image_position(url, soup, image) for image in images[:len(images)/2]]) == len(images)/2:
            return True
        else:
            return False



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





def get_url_title(url):

    pack_file_path = _get_pack_file_path(url)
    # 根据pack,获取对应的title
    title = get_title_from_pack_file(pack_file_path)

    return title


# 获取标记了content的html文件路径
def get_url_tagged_content_html_path(url):
    pack_file_path = _get_pack_file_path(url)
    html_file_path = pack_file_path + ".html"

    if os.path.exists(html_file_path):
        return html_file_path
    else:

        varemark_path = "/home/disk2/wangjianxiang01/tools/varemark"
        cmd = "cd %s && cat %s | ./test_vareamark -t central -o 2 2>stderr.txt | iconv -f gb18030 -t utf-8 > %s"\
              % (varemark_path, pack_file_path, html_file_path)
        os.system(cmd)

        # 需要删除前两行
        cwd = "sed '1, 2d' %s > tmp.txt && mv tmp.txt %s" % (html_file_path, html_file_path)
        os.system(cwd)


        return html_file_path



def _get_pack_file_path(url):
    m = hashlib.md5()
    m.update(url)
    file_name = m.hexdigest()

    pack_file_path = "/home/disk2/wangjianxiang01/BaiduIntern/SPO_url/data/packs/%s" % (file_name)
    if os.path.exists(pack_file_path):
        return pack_file_path
    else:
        # 抓url对应的pack
        wdbtools_path = "/home/disk2/wangjianxiang01/tools/wdbtools/output/client/bin"
        #  抓包 !
        cmd = "%s/seekone '%s' PAGE 2>stderr.txt 1>%s" % (wdbtools_path, url, pack_file_path)
        os.system(cmd)
        #  删除前2行
        cmd = "sed '1, 2d' %s > tmp.txt && mv tmp.txt %s" % (pack_file_path, pack_file_path)
        os.system(cmd)
        return pack_file_path


def get_title_from_pack_file(pack_file):
    # cat pack.test.input | /test_vareamark -t realtitle -o 0 | iconv -f gb18030 -t utf-8
    varemark_path = "/home/disk2/wangjianxiang01/tools/varemark"

    cmd = "cd %s && cat %s | ./test_vareamark -t realtitle -o 0 2>stderr.txt | iconv -f gb18030 -t utf-8" % (varemark_path, pack_file)
    fin = os.popen(cmd)
    result = fin.readlines()

    if result == []:
        return "NULL"

    title = result[-1].strip().split(" | ")[-1]

    return title



if __name__ == '__main__':
    main()
