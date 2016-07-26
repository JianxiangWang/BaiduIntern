#encoding: utf-8
import sys
import os

# 输入url, 判断是不是 小说
def main():
    for line in sys.stdin:
        url = line.strip()


def is_xiaoShuo(url):

    cmd = "../../tools/run_wdbtools-pc.sh %s" % (url)
    print os.popen(cmd)


if __name__ == '__main__':
    is_xiaoShuo("http://www.2828dy.com/bbb/70728.html")