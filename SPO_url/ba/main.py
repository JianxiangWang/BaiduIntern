#!/usr/bin/env python
# encoding: utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import subprocess
import sys, hashlib
import os

# 输入url, 判断是不是 贴吧
def main():

    for line in sys.stdin:
        url = line.strip()
        if is_ba(url):
            title = get_url_title(url)
            S = title
            P = "吧"
            O = url

            print "%s\t%s\t%s\t%s" % (url, S, P, O)


def is_ba(url):

    # 首先, 域名过滤
    if "tieba.baidu.com" not in url:
        return False

    cmd = "../tools/run_wdbtools-pc.sh '%s' 2>../tools/run_wdbtools-pc.stderr" % (url)
    fin = os.popen(cmd)
    result = fin.readlines()[-1]

    print result

    page_type_list = eval(result.strip())

    if {"论坛帖子页"} & set(page_type_list):
        return True
    else:
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



if __name__ == '__main__':
    main()
