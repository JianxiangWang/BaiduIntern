#!/usr/bin/env python
# encoding: utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import subprocess
import sys, hashlib
import os


# 一些PATH
TOOLS_PATH    = "tools"
WDBTOOLS_PATH = "tools/wdbtools/output/client/bin"
VAREMARK_PATH = "tools/varemark"
PACK_PATH     = "/home/disk2/wangjianxiang01/BaiduIntern/SPO_url/data/packs"



# 输入url, 判断是不是 视频
def main():

    for line in sys.stdin:
        url = line.strip()
        if is_shipin(url):
            title = get_url_title(url)
            S = title
            P = "视频"
            O = url

            print "%s\t%s\t%s\t%s" % (url, S, P, O)


def is_shipin(url):

    cmd = "cd %s && ./run_wdbtools-pc.sh '%s' 2>>run_wdbtools-pc.stderr" % (TOOLS_PATH, url)
    fin = os.popen(cmd)
    result = fin.readlines()[-1]

    page_type_list = eval(result.strip())

    if {"视频播放页"} & set(page_type_list):
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
