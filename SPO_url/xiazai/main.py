#!/usr/bin/env python
# encoding: utf-8
import sys
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

    print html_path

    return False

def get_meta_content(soup):
    content = ""
    for meta in soup.find_all("meta"):
        if "content" in meta.attrs:
            content += meta["content"] + "\t"
    return content.strip()



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
