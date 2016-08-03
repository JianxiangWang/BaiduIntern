#!/usr/bin/env python
# coding: utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import os
from pypinyin import lazy_pinyin


def main(template_dir, model_dir, train_P_file):
    index = 1
    for line in open(train_P_file):
        P = line.strip()
        P_pinyi = hanzi_to_pinyi(P)

        print "==" * 40
        print "\t", index, P
        print "==" * 40
        index += 1

        # copy template files
        # init: 符号链接, chmod
        P_dir = "%s/%s" % (model_dir, P_pinyi)

        cmd = "sh -x template.sh %s %s" % (template_dir, P_dir)
        os.system(cmd)

        # 设置与具体P相关
        cmd = "echo '%s' > %s/P" % (P, P_dir)
        os.system(cmd)

        cmd = "echo 'postgresql://jianxiang@localhost:5432/%s_new_data_new_so_DB' > %s/db.url" % (P_pinyi, P_dir)
        os.system(cmd)


def hanzi_to_pinyi(hanzi):
    s = "".join(map(lambda x: x[0].upper() + x[1:], lazy_pinyin(unicode(hanzi))))
    return s[0].lower() + s[1:]


if __name__ == '__main__':
    template_dir = "/home/jianxiang/pycharmSpace/BaiduIntern/zh_deepdive/relations/template_label"
    models_dir   = "/home/jianxiang/pycharmSpace/BaiduIntern/zh_deepdive/relations/models_84P_new_data_new_so"
    train_P_file = "/home/jianxiang/pycharmSpace/BaiduIntern/zh_deepdive/data/train_P.txt"

    main(template_dir, models_dir, train_P_file)