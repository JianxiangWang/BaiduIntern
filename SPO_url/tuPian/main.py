#!/usr/bin/env python
# encoding: utf-8
import sys

import bs4
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
    images = get_all_images(soup)
    # 先获取满足大小的
    satisfied_images = []
    for image in images:
        if "style" in image.attrs:
            dict_style = style_to_dict(image["style"])
            if "height" in dict_style and "weight" in dict_style:
                height = int(dict_style["height"].replace("px", ""))
                weight = int(dict_style["weight"].replace("px", ""))
                if height > 300  and weight > 200:
                    satisfied_images.append(image)

    satisfied_images = satisfied_images[:2]
    if sum([_get_image_position(soup, image) for image in satisfied_images]) >= 1:
        return True
    else:
        # 没有满足条件, 获取所有的前50%图片的位置,判断是不是都在页面的上半部分
        image_num = len(images)

        # 图片数量小于3的, 直接不考虑
        if image_num < 3:
            return False
        # 必须全部在上面
        if image_num >= 3 and image_num <=5:
            if sum([_get_image_position(soup, image) for image in images]) == image_num:
                return True
            else:
                return False
        # 图片数量大于5的
        if sum([_get_image_position(soup, image) for image in images[:len(images)/2]]) == len(images)/2:
            return True
        else:
            return False



def get_all_images(soup):
    images = []
    for content in soup.find_all(attrs={"style": "border:3px solid red;overflow-y:auto;overflow-x:auto;"}):
        for img in content.find_all("img"):
            images.append(img)
    return images


# 1: 在页面的前半部分
# 0: 在页面的后半部分
def _get_image_position(soup, img):
    x = img
    while x.parent != soup.find("body"):
        x = x.parent

    body_children = []
    for child in soup.body.contents:
        if isinstance(child, bs4.element.NavigableString):
            continue
        if child.name == "script":
            continue
        body_children.append(child)

    if body_children.index(x) + 1 / float(len(body_children)) < 0.5:
        return 1
    else:
        return 0

# float:right; height:403px; width:267px
def style_to_dict(style):
    d = {}
    for item in style.split(";"):
        try:
            key, value = item.strip().split(":")
            d[key.strip()] = value.strip()
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

    pack_file_path = os.getcwd() + "/packs/%s" % (file_name)
    if os.path.exists(pack_file_path):
        return pack_file_path
    else:
        # 抓url对应的pack
        wdbtools_path = "/home/disk2/wangjianxiang01/tools/wdbtools/output/client/bin"
        #  抓包 !
        cwd = "%s/seekone %s PAGE 2>stderr.txt 1>%s" % (wdbtools_path, url, pack_file_path)
        os.system(cwd)
        #  删除前2行
        cwd = "sed '1, 2d' %s > tmp.txt && mv tmp.txt %s" % (pack_file_path, pack_file_path)
        os.system(cwd)
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
