#encoding: utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import subprocess
import sys
import os

# 输入url, 判断是不是 小说
def main():
    for line in sys.stdin:
        url = line.strip()
        if is_xiaoShuo(url):
            S = "title"
            P = "体裁/小说"
            O = url

            print("%s\t%s\t%s" % (S, P, O))


def is_xiaoShuo(url):

    cmd = "../tools/run_wdbtools-pc.sh %s" % (url)
    result = subprocess.check_output(cmd, shell=True)
    page_type_list = eval(result.strip())

    print " ".join(page_type_list)
    if {"小说首页", "小说列表页"} & set(page_type_list):
        return True
    else:
        return False



if __name__ == '__main__':
    main()
