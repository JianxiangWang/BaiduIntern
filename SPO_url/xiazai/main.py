#!/usr/bin/env python
# encoding: utf-8
import sys
import bs4
reload(sys)
sys.setdefaultencoding('utf-8')
from bs4 import BeautifulSoup
import subprocess
import sys, hashlib
import os


# 输入url, 判断是不是 下载页
def main():
    for line in sys.stdin:
        url = line.strip()
        if is_xiazai(url):
            title = get_url_title(url)
            S = title
            P = "下载"
            O = url

            print "%s\t%s\t%s\t%s" % (url, S, P, O)


def is_xiazai(url):

    html_path = get_url_tagged_content_html_path(url)
    soup = BeautifulSoup(open(html_path), "html.parser")

    if has_download_a_tag_1(soup) or has_download_a_tag_2(soup):
        return True

    return False


# 1. 正文中, 下载被<a>包围, 至少得有href/onclick/id属性 且href指向的不是html
def has_download_a_tag_1(soup):

    for content in soup.find_all(attrs={"style": "border:3px solid red;overflow-y:auto;overflow-x:auto;"}):
        for a_tag in content.find_all("a"):
            if "下载" in "\t".join(a_tag.stripped_strings):
                # 至少得有这些标签之一
                if set(map(lambda x: x.lower(), a_tag.attrs.keys())) & {"href", "onclick", "id"}:
                    # 如果有href,指向的不能是html, htm
                    if "href" in a_tag.attrs:
                        if not a_tag.attrs["href"].endswith("htm") and not a_tag.attrs["href"].endswith("html") and not a_tag.attrs["href"].endswith("/"):
                            return True
                        else:
                            return False
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
                    if not a_tag.attrs["href"].endswith("htm") and not a_tag.attrs["href"].endswith("html") and not a_tag.attrs["href"].endswith("/"):
                        pass
                    else:
                        flag = 0

                if flag == 1:

                    # 如果父节点是P, a_tag 往上走一步
                    # x = a_tag
                    # while x.parent.name == "p":
                    #     x = x.parent

                    # if a_tag.parent.name == "p":
                    #     a_tag = a_tag.parent


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




def get_url_title(url):

    pack_file_path = _get_pack_file_path(url)
    # 根据pack,获取对应的title
    title = get_title_from_pack_file(pack_file_path)

    return title



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
        cwd = "%s/seekone '%s' PAGE 2>stderr.txt 1>%s" % (wdbtools_path, url, pack_file_path)
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



if __name__ == '__main__':
    main()
