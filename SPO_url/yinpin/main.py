#!python/bin/python
# encoding: utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from bs4 import BeautifulSoup
import subprocess
import sys, hashlib
import os

# 一些PATH
TOOLS_PATH    = "tools"
WDBTOOLS_PATH = "tools/wdbtools/output/client/bin"
VAREMARK_PATH = "tools/varemark"
# PACK_PATH     = "/app/ps/spider/kg-value/wangjianxiang01/packs"
PACK_PATH     = "/home/disk2/wangjianxiang01/BaiduIntern/SPO_url/data/packs"

# 输入url, 判断是不是 音频页
def main():

    for line in sys.stdin:
        url = line.strip()
        if is_shipin(url):
            title = get_url_title(url)
            S = title
            P = "音频"
            O = url

            print "%s\t%s\t%s\t%s" % (url, S, P, O)


def is_shipin(url):

    html_path = get_url_tagged_content_html_path(url)
    soup = BeautifulSoup(open(html_path), "html.parser")

    # 基于meta的识别
    content = get_meta_content(soup)
    if "音乐" not in content and "播放器" not in content and "电台" not in content:
        return False

    # 判断页面是否有播放元素
    if len(soup.find_all("a", attrs={"title": "播放"})) > 0:
        return True

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



# 获取标记了content的html文件路径
def get_url_tagged_content_html_path(url):
    pack_file_path = _get_pack_file_path(url)
    html_file_path = pack_file_path + ".html"

    if os.path.exists(html_file_path):
        return html_file_path
    else:

        cmd = "cd %s && cat %s | ./test_vareamark -t central -o 2 2>>stderr.txt | iconv -f gb18030 -t utf-8 > %s"\
              % (VAREMARK_PATH, pack_file_path, html_file_path)
        os.system(cmd)

        # 需要删除前两行
        cwd = "sed '1, 2d' %s > tmp.txt && mv tmp.txt %s" % (html_file_path, html_file_path)
        os.system(cwd)


        return html_file_path



def _get_pack_file_path(url):
    m = hashlib.md5()
    m.update(url)
    file_name = m.hexdigest()

    pack_file_path = "%s/%s" % (PACK_PATH, file_name)
    if os.path.exists(pack_file_path):
        return pack_file_path
    else:
        #  抓包 !
        cwd = "%s/seekone '%s' PAGE 2>>stderr.txt 1>%s" % (WDBTOOLS_PATH, url, pack_file_path)
        os.system(cwd)
        #  删除前2行
        cwd = "sed '1, 2d' %s > %s.tmp && mv %s.tmp %s" % (pack_file_path, pack_file_path, pack_file_path, pack_file_path)
        os.system(cwd)
        return pack_file_path


def get_title_from_pack_file(pack_file):
    # cat pack.test.input | /test_vareamark -t realtitle -o 0 | iconv -f gb18030 -t utf-8

    cmd = "cd %s && cat %s | ./test_vareamark -t realtitle -o 0 2>>stderr.txt | iconv -f gb18030 -t utf-8" % (VAREMARK_PATH, pack_file)
    fin = os.popen(cmd)
    result = fin.readlines()

    if result == []:
        return "NULL"

    title = result[-1].strip().split(" | ")[-1]

    return title



if __name__ == '__main__':
    main()
